// TO DO
//
// Dans manage change, rebrancher ce qui manque sur les états des autres classes
// Dans replace, voir s'il y a moyen de faire plus intelligent
// Dans le passage input --> texte, voir comment insérer plusieurs lignes
// Comment supprimer un saut de ligne
// Recompiler math jax / ka tex ?
// gérer proprement l'insertion d'input dans latextArea

class LatextArea {

    constructor(targetId, sourceId) {
        // initialisation
        this.parent = document.getElementById(targetId);
        this.textContent = document.getElementById(sourceId).textContent;
        this.elements = [];
        this.parse();
        this.generateDOM();

        // event bindings
        this.parent.ondblclick = () => {
            this.elements.push(new InputElement(this, ""));
            this.generateDOM();
        };

        // gestion du changement de contenu
        this.changed = false;
        this.AJAX_DELAY = .5;
    }

    get text() {
        let str = '';
        for (let element of this.elements) {
            str += element.text;
        }
        return str;
    }

    generateDOM() {
        for (let children of this.parent.children) {
            children.remove();
        }
        for (let element of this.elements) {
            this.parent.appendChild(element.DOM);
        }
    }

    manageChange () {
        if (!this.changed) {
            let cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            let formData = new FormData;
            let request = new XMLHttpRequest();
            
            this.changed = true;

            request.open("POST", documentSaveLink);
            request.setRequestHeader("X-CSRFToken", cSRFToken)

            setTimeout(function () {
                let data = { "docID": docID, "newContent": this.text};

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
    }

    replace(elementSource, elementFinal) {
        for (let i in this.elements) {
            if (this.elements[i] === elementSource) {
                this.elements[i] = elementFinal;
            }
        }
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

class EmptyElement extends LatextAreaElement {
    constructor () {
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

        // auto resize when created
        setTimeout(this.resize.bind(this), 0);
        // auto focus when created
        setTimeout(this.DOM.focus.bind(this.DOM), 0);
    }

    get text () {
        return this.DOM.value;
    }

    resize() {
        this.DOM.style.height = '1em';
        this.DOM.style.height = this.DOM.scrollHeight + "px";
    }


    toTextElement() {
        if (this.DOM.value != "") {
            this.latextArea.replace(this, new TextElement(this.latextArea, this.DOM.value));
        }
        else {
            this.latextArea.replace(this, new EmptyElement());
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

    toInput() {
        let newElement = new InputElement(this.latextArea, this.textContent);
        this.latextArea.replace(this, newElement);
    }

}
