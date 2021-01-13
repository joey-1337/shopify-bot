#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <iostream>
#include <v8pp/context.hpp>
#include <libplatform/libplatform.h>
#include <v8.h>

//not using a namespace to make it easier to differentiate
//v8pp and v8 objects

struct ContextInfo {

    v8::Isolate * isolate_ptr;
    v8pp::context * ctx_ptr;
};

template<class T> static inline T* xalloc(T*& ptr, size_t x = sizeof(T))
{
    void *tmp = malloc(x);
    if (tmp == NULL) {
        fprintf(stderr, "malloc failed. Aborting");
        abort();
    }
    ptr = static_cast<T*>(tmp);
    return static_cast<T*>(ptr);
}

enum BinaryTypes {
    type_invalid   =   0,
    type_null      =   1,
    type_bool      =   2,
    type_integer   =   3,
    type_double    =   4,
    type_str_utf8  =   5,
    type_array     =   6,
    type_hash      =   7,
    type_date      =   8,

    type_function  = 100,

    type_execute_exception = 200,
    type_parse_exception   = 201,
};

struct BinaryValue {
    union {
        BinaryValue **array_val;
        BinaryValue **hash_val;
        char *str_val;
        uint32_t int_val;
        double double_val;
    };
    enum BinaryTypes type = type_invalid;
    size_t len;
};

void BinaryValueFree(BinaryValue *v) {
    if (!v) {
        return;
    }
    switch(v->type) {
    case type_execute_exception:
    case type_parse_exception:
    case type_str_utf8:
        free(v->str_val);
        break;
    case type_array:
        for (size_t i = 0; i < v->len; i++) {
            BinaryValue *w = v->array_val[i];
            BinaryValueFree(w);
        }
        free(v->array_val);
        break;
    case type_hash:
        for(size_t i = 0; i < v->len; i++) {
            BinaryValue *k = v->hash_val[i*2];
            BinaryValue *w = v->hash_val[i*2+1];
            BinaryValueFree(k);
            BinaryValueFree(w);
        }
        free(v->hash_val);
        break;
    case type_bool:
    case type_double:
    case type_date:
    case type_null:
    case type_integer:
    case type_function: // no value implemented
    case type_invalid:
        // the other types are scalar values
        break;
    }
    free(v);
}

static std::string get_lib_path () {

    std::string str = "placeholder";
    return str;
}

static void init_v8 () {

    static v8::Platform * current_platform = NULL;

    if (current_platform == NULL) {
        v8::V8::InitializeICU();
        current_platform = v8::platform::CreateDefaultPlatform();
        v8::V8::InitializePlatform(current_platform);
        v8::V8::Initialize();
    }
}

ContextInfo * MiniRacer_init_context () {
     
    init_v8();

    ContextInfo* context_info = xalloc(context_info);
    v8pp::context * ctx = new v8pp::context; //must be allocated on the heap.

    context_info->ctx_ptr = ctx;
    context_info->isolate_ptr = ctx->isolate();
    return context_info;
}


BinaryValue * convert_v8_to_binary(ContextInfo* ctx_info, v8::Handle<v8::Value> &value) 
{
    v8::Isolate* isolate = ctx_info->isolate_ptr; 
    BinaryValue* res = new (xalloc(res)) BinaryValue();

    if (value->IsNull() || value->IsUndefined()) {
        res->type = type_null;
    }

    else if (value->IsInt32()) {
        res->type = type_integer;
        auto val = value->Uint32Value();
        res->int_val = val;
    }

    // ECMA-262, 4.3.20
    // http://www.ecma-international.org/ecma-262/5.1/#sec-4.3.19
    else if (value->IsNumber()) {
        res->type = type_double;
        double val = value->NumberValue();
        res->double_val = val;
    }

    else if (value->IsBoolean()) {
        res->type = type_bool;
        res->int_val = (value->IsTrue() ? 1 : 0);
    }

    else if (value->IsArray()) {
        v8::Local<v8::Array> arr = v8::Local<v8::Array>::Cast(value);
        size_t len = arr->Length();
        BinaryValue **ary = xalloc(ary, sizeof(*ary) * len);

        res->type = type_array;
        res->array_val = ary;

        for(uint32_t i = 0; i < arr->Length(); i++) {
            v8::Local<v8::Value> element = arr->Get(i);
            BinaryValue *bin_value = convert_v8_to_binary(ctx_info, element);
            if (bin_value == NULL) {
                goto err;
            }
            ary[i] = bin_value;
            res->len++;
        }
    }

    else if (value->IsFunction()){
        res->type = type_function;
    }
    else if (value->IsObject()) {
        res->type = type_hash;

        v8::HandleScope handle_scope(isolate);
        v8::TryCatch trycatch(isolate);

        v8::Local<v8::Object> object = value->ToObject();
        v8::MaybeLocal<v8::Array> maybe_props = object->GetOwnPropertyNames();
        if (!maybe_props.IsEmpty()) {
            v8::Local<v8::Array> props = maybe_props.ToLocalChecked();
            uint32_t hash_len = props->Length();

            if (hash_len > 0) {
                res->hash_val = xalloc(res->hash_val,
                                       sizeof(*res->hash_val) * hash_len * 2);
            }

            for (uint32_t i = 0; i < hash_len; i++) {
                v8::Local<v8::Value> pkey = props->Get(i);
                v8::Local<v8::Value> pvalue = object->Get(pkey);
                // this may have failed due to Get raising

                if (trycatch.HasCaught()) {
                    // TODO: factor out code converting exception in
                    //       nogvl_context_eval() and use it here/?
                    goto err;
                }

                BinaryValue *bin_key = convert_v8_to_binary(ctx_info, pkey);
                BinaryValue *bin_value = convert_v8_to_binary(ctx_info, pvalue);

                if (!bin_key || !bin_value) {
                    BinaryValueFree(bin_key);
                    BinaryValueFree(bin_value);
                    goto err;
                }

                res->hash_val[i * 2]     = bin_key;
                res->hash_val[i * 2 + 1] = bin_value;
                res->len++;
            }
        } // else empty hash
    }

    else if (value->IsDate()) {
        res->type = type_date;
        v8::Local<v8::Date> date = v8::Local<v8::Date>::Cast(value);

        double timestamp = date->ValueOf();
        res->double_val = timestamp;
    }  

    else {
        v8::Local<v8::String> rstr = value->ToString();

        res->type = type_str_utf8;
        res->len = size_t(rstr->Utf8Length()); // in bytes
        size_t capacity = res->len + 1;
        res->str_val = xalloc(res->str_val, capacity);
        rstr->WriteUtf8(res->str_val);
    }
    return res;

err:
    BinaryValueFree(res);
    return NULL;
}

static BinaryValue* MiniRacer_eval_context(ContextInfo* ctx_info, char *utf_str, int str_len)
{
    v8::Local<v8::Value> tmp = ctx_info->ctx_ptr->run_script(utf_str);
    auto res = convert_v8_to_binary(ctx_info, tmp);
    return res;
}

static void uninitialize_v8 ()
{
    v8::V8::Dispose();
    v8::V8::ShutdownPlatform();
}

extern "C" {

BinaryValue* mr_eval_context(ContextInfo * ctx_info, char * str, int len) {
    
    v8::HandleScope handleScope(ctx_info->isolate_ptr);
    BinaryValue* res = MiniRacer_eval_context(ctx_info, str, len);
    return res;
}

ContextInfo* mr_init_context () {
    ContextInfo* ctx_info = MiniRacer_init_context();
    return ctx_info;
}

void dispose_v8 () {uninitialize_v8 ();}

//TODO... actually implement these functions
//not a super pressing matter though
//for now they are here to not crash
//the python extension

void mr_free_value() {}

void mr_heap_stats () {}

void mr_low_memory_notification () {}

void mr_heap_snapshot () {}

void mr_free_context () {}

}


