class AudioContentManager {

    constructor(maxItems = 8) {
        this.DOM = document.getElementById("responseDisplay");
        this.maxItems = maxItems;
        this.elements = [];
    }


    addElement(content) {
        let element = document.createElement("span");
        element.onclick = function (evt) {
            insertAtCursor(content);
            audioContentManager.reset();
            chunks = [];
        }
        element.appendChild(document.createTextNode(content));
        this.DOM.appendChild(element);
        this.DOM.appendChild(document.createElement("br"));
        this.adaptDOMPosition();
    }

    adaptDOMPosition() {

    }

    manageAJAXResponse(response) {
        let element;
        audioContentManager.reset();
        if (response.instruction == "propose") {
            for (let i = 0; i < response.content.length && i < this.maxItems; i++) {
                audioContentManager.addElement(response.content[i]);
            }
        }
    }

    reset() {
        while (this.DOM.hasChildNodes()) {
            this.DOM.removeChild(this.DOM.firstChild);
        }
    }

}

var audioContentManager = new AudioContentManager();
