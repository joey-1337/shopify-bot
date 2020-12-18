
class HTMLCollection extends Array {
    item (index) {return this[index]}
}

/*
var EventTarget {
    addEventListener: function addEventListener () {return null;},
    removeEventListener: function removeEventListener() {return null;}, 
    dispatchEvent: function dispatchEvent () {return null;},
};
*/


var Node  = {
    baseURi : DOMString,
    childNodes : Nodelist,
    firstChild : Node,
    isConnected : Boolean,
    lastChild : Node,
    nextSibling : Node,
    nodeName : DOMString,
    nodeType : Number,
    nodeValue : String,
    ownerDocument : document,
    parentNode : Node,
    parentElement : Element,
    previousSibling : Node,
    textContent : String,

    //TODO... methods
};

var parentNode = {} //todo

var HTMLDocument = Document;
var document = Document;

Node = {...Event,...Node};

var Document = {
    acnhors : HTMLCollection,
    body : Node,
    characterSet : string,
    compatMode : string,
    contentType : string,
    doctype : DocumentType,
    documentElement : Element,
    documentURI : string,
    embeds : HTMLCollection,
    fonts : FontFaceSet,
    forms : HTMLCollection,
    head : HTMLHeadElement,
    hidden : Boolean,
    images : HTMLCollection,
    implementation : DOMImplementation,
    lastStyleSheetSet : document.selectedStyleSheetSet,
    links : HTMLCollection,
    mozSyntheticDocument : false,
    pictureInPictureEnabled : Boolean,
    plugins : HTMLCollection,
    featurePolicy : FeaturePolicy,
    scripts : HTMLCollection,
    scrollingElement : Element,
    timeline : DocumentTimeline,
    visibilityState : string, //visible, hidden, prerender, or unloaded important to spoof page rendering.
    cookie: string,
    defaultView: window,
    designMode : "off",
    dir : DOMString,
    domain : string,
    lastModified : string, //basically just the time.
    location : string, //the document's uri 
    readyState : string, //loading, interactive, complete
    referrer : string,
    title : string, 
    URL : string,
    

};

Document = {...Node,...parentNode,...HTMLDocument,...Document};


