// TO DO
//
// Dans manage change, rebrancher ce qui manque sur les états des autres classes
// Comment supprimer un saut de ligne
// Recompiler math jax / ka tex ?
// meilleure gestion de l'audio continu

class LatextArea {

    constructor(targetId, sourceId) {
        // initialisation
        this.parent = document.getElementById(targetId);
        this.textContent = document.getElementById(sourceId).textContent;
        this.elements = [];
        this.killNextAudio = false;
        this.parse();
        this.generateDOM();

        // event bindings
        document.getElementById("start_rec").onclick = () => {
            sendContinuousAudio(500, voiceAnalysisLink, true, this.audioResponseManager.bind(this));
        };

        // gestion du changement de contenu
        this.changed = false;
        this.AJAX_DELAY = .5;
    }

    get activeElement () {
        for (let element of this.elements) {
            if (element.DOM == document.activeElement) return element;
        }
        for (let i = this.elements.length -1 ; i >= 0; i--)
            if (this.elements[i] instanceof TextElement || 
                this.elements[i] instanceof InputElement)
                    return this.elements[i];
    }

    get text() {
        let str = '';
        for (let element of this.elements) {
            str += element.text;
        }
        return str;
    }

    audioResponseManager (response){
        if (this.killNextAudio) {
            this.killNextAudio = false;
            return;
        }
        if (response.instruction == "propose") {
            if (this.audioResponseElement == undefined) {
                this.audioResponseElement = 
                new AudioResponseElement(this, response.content);
            } 
            else 
                this.audioResponseElement.updateChoices(response.content);
        }
    }

    generateDOM() {
        if (this.elements.length == 0) {
            this.elements.push(new TextElement(this, ""));
        }
        for (let children of this.parent.children) {
            children.remove();
        }
        for (let element of this.elements) {
            if (element instanceof EmptyElement == false) {
                this.parent.appendChild(element.DOM);
            }

        }
    }

    manageChange() {
        if (!this.changed) {
            let cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            let formData = new FormData;
            let request = new XMLHttpRequest();

            this.changed = true;

            request.open("POST", documentSaveLink);
            request.setRequestHeader("X-CSRFToken", cSRFToken)

            setTimeout(function () {
                let data = { "docID": docID, "newContent": this.text };

                this.changed = false;

                communicationIndicatorManager.addRequest();
                // contentStateManager.newState(data.newContent);
                data = JSON.stringify(data);
                formData.append("data", data);
                request.send(formData);
                request.onreadystatechange = function () {
                    if (request.readyState == 4 && request.status == 200) {
                        communicationIndicatorManager.endRequest();
                    }
                }
                // manageQueueButtonsStyle();
            }.bind(this), 1000 * this.AJAX_DELAY);
        }
    }

    parse() {
        let contentByLine = this.textContent.split("\n");
        for (let line of contentByLine) {
            let textElement = new TextElement(this, line);
            this.elements.push(textElement);
            this.elements.push(new NewLineElement(this));
        }
        if (this.elements.length != 0)
            this.elements.pop();
    }

    replace(elementToReplace, newElements = undefined) {
        /*
            Replaces elementToReplace in this.elements
            newElements can be either :
                - undefined : in this case, elementsToReplace will just be deleted
                - an instance of LatextAreaElement
                - an array of instances of LatextAreaElement
        */

        let indexToReplace = this.elements.indexOf(elementToReplace);
        let start = this.elements.slice(0, indexToReplace);
        let end = this.elements.slice(indexToReplace + 1);

        this.elements = [];
        for (let element of start) this.elements.push(element);

        if (newElements == undefined) {
            /* Nothing happens */
        }
        else if (newElements instanceof LatextAreaElement) {
            this.elements.push(newElements);
        }
        else {
            for (let element of newElements) this.elements.push(element);
        }

        for (let element of end) this.elements.push(element);
        // un peu couteux, voir s'il n'y a pas plus simple
        this.generateDOM();
    }

}

class LatextAreaElement {

    constructor(latextArea, text) {
        this.latextArea = latextArea;
        this.textContent = text;
        this.DOM = document.createElement("span");
    }

    get text() {
        return this.textContent;
    }

}

class AudioResponseElement extends LatextAreaElement {
    
    constructor (latextArea, choices, maxElements = 8) {
        super(latextArea, '');
        this.maxElements = maxElements;
        this.updateChoices(choices);
    }

    build () {
        let DOM = document.createElement('div');
        DOM.className = "audio-choice";
        for (let i=0; i < this.choices.length && i < this.maxElements; i++) {
            let span = document.createElement('span');
            span.onclick = () => {
                this.choose(this.choices[i]);
                this.destroy();
            };
            span.innerHTML = this.choices[i];
            DOM.appendChild(span);
            DOM.appendChild(document.createElement('br'));
        }
        DOM.style.position = "absolute";
        let rect = this.latextArea.activeElement.DOM.getBoundingClientRect();
        DOM.style.top = (rect.top + rect.height) + "px";
        DOM.style.left = (rect.left)+ "px";
        try {
            this.DOM.remove();
        }
        catch (error) {}
        this.DOM = DOM;
        document.body.appendChild(this.DOM);
    }

    choose(choice) {
        this.latextArea.activeElement.insert(choice);
    }

    destroy (){
        this.DOM.remove();
        this.latextArea.audioResponseManager = undefined;
        this.latextArea.killNextAudio = true;
        document.getElementById("stop_rec").click();
    }

    updateChoices (choices) {
        this.choices = choices;
        this.build();
    }

}

class EmptyElement extends LatextAreaElement {
    constructor() {
        // initialisation
        super(undefined, "");
    }
}

class InputElement extends LatextAreaElement {

    constructor(latextArea, text) {
        // initialisation
        super(latextArea, text);
        this.DOM = document.createElement("textArea");
        this.DOM.value = text;
        // event bindings
        this.DOM.onblur = this.toTextElement.bind(this);
        this.DOM.oninput = () => {
            this.resize();
            this.latextArea.manageChange();
        };
        this.DOM.onkeydown = this.mouvementHandler.bind(this);

        // auto resize when created
        setTimeout(this.resize.bind(this), 0);
        // auto focus when created
        setTimeout(this.DOM.focus.bind(this.DOM), 0);
    }

    get text() {
        return this.DOM.value;
    }

    insert (value) {
        if (this.DOM.value != "" && this.DOM.value.substr(this.DOM.value.length - 1) != " ") {
            value = " " + value;
        }
        this.DOM.value += value;
        this.latextArea.manageChange();
    }

    resize() {
        this.DOM.style.height = '1em';
        this.DOM.style.height = this.DOM.scrollHeight + "px";
    }

    toTextElement() {
        if (this.DOM.value != "") {
            if (this.DOM.value.indexOf('\n') == -1)
                this.latextArea.replace(this, new TextElement(this.latextArea, this.DOM.value));
            else {
                let values = this.DOM.value.split('\n');
                let elements = [];
                for (let value of values) {
                    elements.push(new TextElement(this.latextArea, value));
                    elements.push(new NewLineElement(this.latextArea));
                }
                if (elements.length != 0)
                    elements.pop();
                this.latextArea.replace(this, elements);
            }
        }
        else {
            this.latextArea.replace(this);
            // this.latextArea.replace(this, new EmptyElement());
        }

    }

    mouvementHandler(event) {
        var positionCurseur = this.DOM.selectionStart;
        var longueur = this.DOM.value.length;
        var nbLines = (this.DOM.value.match(/\n/g)||[]).length + 1;
        var currentLine = -1* ((this.DOM.value.substring(positionCurseur).match(/\n/g)||[]).length - nbLines);
        if (event.keyCode == 37 && positionCurseur==0) {
            let indexFocus = this.latextArea.elements.indexOf(this)-2;
            if (indexFocus >= 0) {
                this.latextArea.elements[indexFocus].toInput();
                this.toTextElement();
            }
        }
        if (event.keyCode == 39 && positionCurseur-longueur==0) {
            let indexFocus = this.latextArea.elements.indexOf(this)+2;
            if (indexFocus < this.latextArea.elements.length) {
                this.latextArea.elements[indexFocus].toInput();
                this.toTextElement();
            }
        }
        if (event.keyCode == 38 && currentLine==1) {
            let indexFocus = this.latextArea.elements.indexOf(this)-2;
            if (indexFocus >= 0) {
                this.latextArea.elements[indexFocus].toInput();
                this.toTextElement();
            }
        }
        if (event.keyCode == 40 && currentLine==nbLines) {
            let indexFocus = this.latextArea.elements.indexOf(this)+2;
            if (indexFocus < this.latextArea.elements.length) {
                this.latextArea.elements[indexFocus].toInput();
                this.toTextElement();
            }
        }
    }

}

class NewLineElement extends LatextAreaElement {

    constructor(latextArea) {
        super(latextArea, '\n');
        this.DOM = document.createElement('br');
    }

}

class TextElement extends LatextAreaElement {

    constructor(latextArea, text) {
        // initialisation
        super(latextArea, text);
        this.DOM = document.createElement("span");
        this.DOM.innerHTML = text;
        this.DOM.className = "latext-element";

        // event bindings
        this.DOM.onclick = this.toInput.bind(this);
    }

    insert (value) {
        if (this.DOM.innerText != "" && this.DOM.innerText.substr(this.DOM.innerText.length - 1) != " ") {
            value = " " + value;
        }
        this.DOM.innerText += value;
        this.textContent += value;
        this.latextArea.manageChange();
    }

    toInput() {
        let newElement = new InputElement(this.latextArea, this.textContent);
        this.latextArea.replace(this, newElement);
    }

}
