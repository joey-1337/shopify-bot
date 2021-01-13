#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <iostream>
#include <v8pp/context.hpp>
#include <libplatform/libplatform.h>
#include <v8.h>

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

struct ContextInfo {

    v8::Isolate * isolate_ptr;
    v8pp::context * ctx_ptr;
};

v8::Local<v8::Value> MiniRacer_eval_context(ContextInfo * ctx_info, char *utf_str, int str_len) //the last arg only exists
{                                                                                               //to make python happy
    v8::Local<v8::Value> tmp = ctx_info->ctx_ptr->run_script(utf_str);
    return tmp;
}


void init_v8 () {
    
    static v8::Platform * current_platform = NULL;    

    if (current_platform == NULL) {
        v8::V8::InitializeICU();
        current_platform = v8::platform::CreateDefaultPlatform();
        v8::V8::InitializePlatform(current_platform);
        v8::V8::Initialize();
    }
}

ContextInfo * mr_init_ctx () {

    init_v8();

    ContextInfo* context_info = xalloc(context_info); 
    v8pp::context * ctx = new v8pp::context; //must be allocated on the heap.

    context_info->ctx_ptr = ctx;
    context_info->isolate_ptr = ctx->isolate();
    return context_info;
}


int main ()
{
    ContextInfo * ctx_info = mr_init_ctx();
    v8::HandleScope handleScope(ctx_info->isolate_ptr); //MUST BE INITIALIZED ON THE STACK BEFORE CALLING
                                                        //MiniRacer_eval_context(), only the stack part
                                                        //really makes sense to me, but I am past the 
                                                        //phase where I question the infinite wisdom
                                                        //of the v8 engine

    auto tmp = MiniRacer_eval_context(ctx_info, "1*6", 3);
    v8::String::Utf8Value resultString(ctx_info->ctx_ptr->isolate(), tmp);
    std::cout << "The result of the script was: " << *resultString << "\n";
    return 0;
}
