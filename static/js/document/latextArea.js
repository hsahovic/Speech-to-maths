class LatextArea {

    constructor(targetId, sourceId) {
        this.parent = document.getElementById(targetId);
        this.textContent = document.getElementById(sourceId).textContent;
        this.elements = [];

        this.parse();
        this.generateDOM();
        console.log(this.text);
    }

    parse() {
        let contentByLine = this.textContent.split("\n");
        for (let line of contentByLine) {
            let textElement = new TextElement(this, line);
            this.elements.push(textElement);
            this.elements.push(new NewLineElement(this));
        }
    }

    generateDOM() {
        for (children of this.parent.children) {
            children.remove();
        }
        for (let element of this.elements) {
            this.parent.appendChild(element.DOM);
        }
    }

    get text() {
        let str = "";
        for (let element of this.elements) {
            str += element.text;
        }
        return str;
    }

    // methode replace à implementer
    // permet de remplacer un element par un autre :
        // 1) Dans la liste d'elements de textArea
        // 2) Dans le DOM

}

class LatextAreaElement {

    constructor(latextArea, text) {
        this.latextArea = latextArea;
        this.textContent = text;
    }

    get text() {
        return this.textContent;
    }

}

class NewLineElement extends LatextAreaElement {

    constructor(latextAreat) {
        super(latextArea,'\n');
        this.DOM = document.createElement('br');
    }

}

class TextElement extends LatextAreaElement {

    constructor(latextArea, text) {
        super(latextArea,text);
        this.DOM = document.createElement("span");
        this.DOM.innerHTML = text;
        this.DOM.onclick = this.selected.bind(this);
    }

    selected () {
        console.log("Clicked on ", this.textContent);
    }

}

// créer InputElement