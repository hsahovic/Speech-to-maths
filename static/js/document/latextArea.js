// TO DO
//
// Dans manage change, rebrancher ce qui manque sur les états des autres classes
// Comment supprimer un saut de ligne
// meilleure gestion de l'audio continu

AJAX_DELAY = 1; // Delay in seconds

function insertAtCursor(value, field = document.getElementsByName('content')[0]) {
    // Permet de remplacer la selection par ou inserer au curseur, ou le cas échéant, à la fin de contenu, value
    // IE
    if (document.selection) {
        field.focus();
        sel = document.selection.createRange();
        sel.text = value;
    }
    //MOZILLA and others
    else if (field.selectionStart || field.selectionEnd) {
        var startPos = field.selectionStart;
        var endPos = field.selectionEnd;
        field.value = field.value.substring(0, startPos)
            + value
            + field.value.substring(endPos, field.value.length);
        field.selectionStart = startPos + value.length;
        field.selectionEnd = startPos + value.length;
    }
    else {
        field.value += value;
    }
    manageContentChange();
}

class LatextArea {

    constructor(targetId, sourceId) {
        // initialisation
        this.parent = document.getElementById(targetId);
        this.textContent = document.getElementById(sourceId).textContent;
        this.editionMode = 1;
        // Edition mode 1 is preview mode
        //              2 is LaTeX code mode
        this.elements = [];
        this.killNextAudio = false;
        this.choiceHappened = false;

        this.parse();
        this.generateDOM();

        // event bindings
        document.getElementById("start_rec").onclick = () => {
            sendContinuousAudio(500, voiceAnalysisLink, true, this.audioResponseManager.bind(this));
        };
        document.getElementById("edition-preview").onclick = () => {
            this.switchEditionMode(1);
            document.getElementById("edition-preview").className = "text-editor-button selected-mode";
            document.getElementById("edition-code").className = "text-editor-button";
        };
        document.getElementById("edition-code").onclick = () => {
            this.switchEditionMode(2);
            document.getElementById("edition-preview").className = "text-editor-button";
            document.getElementById("edition-code").className = "text-editor-button selected-mode";
        };

        // gestion du changement de contenu
        this.changed = false;
        this.ajaxDelay = AJAX_DELAY;
    }

    get activeElement() {
        for (let line of this.elements) {
            for (let element of line) {
                if (element.DOM == document.activeElement) return element;
            }
        }
        for (let i = this.elements.length - 1; i >= 0; i--)
            for (let j = this.elements[i].length - 1; j >= 0; j--)
                if (this.elements[i][j] instanceof TextElement ||
                    this.elements[i][j] instanceof InputElement)
                    return this.elements[i][j];
    }

    get inputElement() {
        for (let i = this.elements.length - 1; i >= 0; i--)
            for (let j = this.elements[i].length - 1; j >= 0; j--)
                if (this.elements[i][j] instanceof InputElement)
                    return this.elements[i][j];
    }

    get text() {
        if (this.editionMode == 1) {
            let str = '';
            for (let line of this.elements) {
                for (let element of line) {
                    if (!(element instanceof NewLineElement) || (element.lineBreak)) {
                        str += element.text;
                    }
                    else {
                        str += ' ';
                    }
                }
            }
            return str;
        }
        else if (this.editionMode == 2) {
            return this.DOM.value;
        }
    }

    audioResponseManager(response) {
        if (this.killNextAudio) {
            this.killNextAudio = false;
            return;
        }
        if (response.instruction == "propose") {
            if (this.audioResponseElement == undefined) {
                this.audioResponseElement =
                    new AudioResponseElement(this, response.content, response.token);
            }
            else if (this.choiceHappened == false)
                this.audioResponseElement.updateChoices(response.content, response.token);
            else 
                this.choiceHappened = false;
        }
    }

    findIndexes(element) {
        let resi = -1;
        let resj = -1;
        for (let i = 0; i < this.elements.length; i++) {
            for (let j = 0; j < this.elements[i].length; j++) {
                if (element === this.elements[i][j]) {
                    resi = i;
                    resj = j;
                }
            }
        }
        return [resi, resj];
    }

    generateDOM() {
        while (this.parent.children.length != 0)
            this.parent.children[0].remove();

        if (this.editionMode == 1) {
            if (this.elements.length == 0) {
                this.elements.push([new TextElement(this, "")]);
            }
            for (let line of this.elements) {
                for (let element of line) {
                    if (element == undefined) { // We've got problems with empty strings repeatedly parsed ; this is a (messy) fix
                        this.elements[0][0] = new TextElement(this, "");
                        this.parent.appendChild(this.elements[0][0].DOM);
                    }
                    else if (element instanceof EmptyElement == false) {
                        this.parent.appendChild(element.DOM);
                    }
                }
            }
        }
        else if (this.editionMode == 2) {
            this.DOM = document.createElement("textarea");
            this.DOM.value = this.textContent;
            this.DOM.className = "documentTextAreaEditor";
            this.DOM.oninput = () => {
                this.manageChange();
            };
            this.parent.appendChild(this.DOM);
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
            }.bind(this), 1000 * this.ajaxDelay);
        }
    }

    merge(firstElement, secondElement) {
        let iFirst = this.findIndexes(firstElement)[0];
        let jFirst = this.findIndexes(firstElement)[1];
        let iSecond = this.findIndexes(secondElement)[0];
        let jSecond = this.findIndexes(secondElement)[1];
        if (iFirst != iSecond) {
            this.mergeLines(this.elements[iFirst], this.elements[iSecond]);
        }
        let start = this.elements.slice(0, iFirst);
        let end = this.elements.slice(iSecond + 1);

        let mergedElement = new TextElement(this, firstElement.text + secondElement.text);

        this.elements[iFirst].splice(jFirst, 2, mergedElement);
        firstElement.DOM.remove();
        secondElement.DOM.remove();
        if (this.elements[iFirst].length > jFirst + 1) {
            this.parent.insertBefore(mergedElement.DOM, this.elements[iFirst][jFirst + 1].DOM);
        } else if (this.elements.length > iFirst + 1) {
            this.parent.insertBefore(mergedElement.DOM, this.elements[iFirst + 1][jFirst].DOM);
        } else {
            this.parent.appendChild(mergedElement.DOM);

        }
    }

    mergeLines(firstLine, secondLine) {
        let indexFirst = this.elements.indexOf(firstLine);
        let indexSecond = this.elements.indexOf(secondLine);

        let mergedLine = this.elements[indexFirst].concat(this.elements[indexSecond]);
        this.elements.splice(indexFirst, 3, mergedLine);
        for (let element of firstLine) element.DOM.remove();
        for (let element of secondLine) element.DOM.remove();
        if (this.elements.length > indexFirst + 1) {
            for (let element of mergedLine) this.parent.insertBefore(element.DOM, this.elements[indexFirst + 1][0].DOM);
        } else {
            for (let element of mergedLine) this.parent.appendChild(element.DOM);

        }
    }

    parse() {
        this.elements = [];

        let patt = /(\$\$[^\$]*\$\$|\$[^\$]*\$)/g;
        
        if (this.editionMode == 1) {
            let contentByLine = this.textContent.split(/\n/);
            for (let line of contentByLine) {
                let contentLine = line.split(/\{breaK\}/);
                let textElement;
                let textLine = [];
                
                line = line.replace(patt, "{breaK}$&{breaK}");

                for (let element of contentLine) {
                    if (element[0] == '\$') {
                        textElement = new MathElement(this, element);
                        textLine.push(textElement);
                    } else {
                        textElement = new TextElement(this, element);
                        textLine.push(textElement);
                    }
                }
                this.elements.push(textLine);
                this.elements.push([new NewLineElement(this, true)]);
            }
            if (this.elements.length != 0)
                this.elements.pop();
            this.elements[0][0].toInput();
        }
        else if (this.editionMode == 2) {
            return;
        }
    }

    replaceElement(elementToReplace, newElement = undefined) {
        /*
            Replaces elementToReplace in this.elements
            newElement can be either :
                - undefined : in this case, elementsToReplace will just be deleted
                - an instance of LatextAreaElement
                - a array of elements
        */
        let iToReplace = this.findIndexes(elementToReplace)[0];
        let jToReplace = this.findIndexes(elementToReplace)[1];
        elementToReplace.DOM.remove();
        if (newElement == undefined) {
            this.elements[iToReplace].splice(jToReplace, 1);
        } else if (newElement instanceof LatextAreaElement) {
            this.elements[iToReplace].splice(jToReplace, 1, newElement);
        } else {
            this.elements[iToReplace].splice(jToReplace, 1, newElement[0]);
            for (let compt = 1; compt < newElement.length; compt++) {
                this.elements[iToReplace].splice(jToReplace + compt, 0, newElement[compt]);
            }
        }
        // un peu couteux, voir s'il n'y a pas plus simple
        this.generateDOM();
    }

    replaceLine(lineToReplace, newLines = undefined) {
        /*
            Replaces lineToReplace in this.elements
            newLines can be either :
                - undefined : in this case, linesToReplace will just be deleted
                - an array of instances of LatextAreaElement
                - multiple arrays of LatextAreaElement
        */
        let indexToReplace = this.elements.indexOf(lineToReplace);
        let startLine = this.elements.slice(0, indexToReplace);
        let endLine = this.elements.slice(indexToReplace + 1);
        for (let element of lineToReplace) element.DOM.remove();

        this.elements = [];
        for (let line of startLine) this.elements.push(line);
        if (newLines == undefined) {
            /* Nothing happens */
        }
        else if (newLines[0] instanceof LatextAreaElement) {
            this.elements.push(newLines);
        }
        else {
            for (let line of newLines) this.elements.push(line);
        }
        for (let line of endLine) this.elements.push(line);
        this.generateDOM();
    }

    switchEditionMode(mode) {
        if (this.editionMode != mode) {
            this.textContent = this.text;
            this.editionMode = mode;
            this.parse();
            this.generateDOM();
        }
    }

}


class LatextAreaElement {

    constructor(latextArea, text, position) {
        this.latextArea = latextArea;
        this.textContent = text;
        if (position != undefined) {
            this.iCurseur = position;
        } else {
            this.iCurseur = 0;
        }
        this.DOM = document.createElement("span");
    }

    get text() {
        return this.textContent;
    }

    get curseur() {
        return this.iCurseur;
    }

    get curseurLigne() {
        var i = this.latextArea.findIndexes(this)[0];
        var j = this.latextArea.findIndexes(this)[1];
        var positionCurseurLine = this.curseur;
        for (let k = 0; k < j; k++) positionCurseurLine += this.latextArea.elements[i][k].textContent.length;
        return positionCurseurLine;
    }

    findIndexes() {
        let resi = -1;
        let resj = -1;
        for (let i = 0; i < this.latextArea.elements.length; i++) {
            for (let j = 0; j < this.latextArea.elements[i].length; j++) {
                if (this === this.latextArea.elements[i][j]) {
                    resi = i;
                    resj = j;
                }
            }
        }
        return [resi, resj];
    }

    resizeForward() {
        //this.DOM.style.height = '1em';
        var compteur = 0;
        this.setSize();
        var change = false;
        var i = this.latextArea.findIndexes(this)[0];
        let width = this.latextArea.elements[0][0].DOM.offsetLeft;
        for (let element of this.latextArea.elements[i]) {
            width += element.DOM.offsetWidth;
        }
        let parentWidth = this.DOM.parentElement.offsetWidth;
        while (width > parentWidth) {
            if (compteur == 100) { break; }
            compteur++;
            var l = this.latextArea.elements[i].length - 1; // changer nom
            var elementCoupe = this.latextArea.elements[i][l];
            var positionDernierMot = Math.max(elementCoupe.text.lastIndexOf(' '), elementCoupe.text.lastIndexOf("&nbsp"));
            var str1 = elementCoupe.text.substring(0, positionDernierMot);
            var str2 = elementCoupe.text.substring(positionDernierMot + 1);
            width -= elementCoupe.DOM.offsetWidth;
            if (elementCoupe instanceof InputElement) {
                elementCoupe.iCurseur = elementCoupe.DOM.selectionEnd;  // changer nom 
            }
            elementCoupe.setText(str1);
            if (this.latextArea.elements.length > i + 2) {  // On choisit où rajouter ce qui dépasse
                if (this.latextArea.elements[i + 1][0].lineBreak) {  // Si on a un saut de ligne on crée une nouvelle ligne 
                    this.latextArea.elements.splice(i + 1, 0, [new NewLineElement(this.latextArea)], [new TextElement(this.latextArea, str2)]);
                    this.latextArea.parent.insertBefore(latextArea.elements[i + 1][0].DOM, latextArea.elements[i + 3][0].DOM);
                    this.latextArea.parent.insertBefore(latextArea.elements[i + 2][0].DOM, latextArea.elements[i + 3][0].DOM);
                } else {
                    this.latextArea.elements[i + 2][0].setText(str2 + ' ' + this.latextArea.elements[i + 2][0].textContent); // Sinon on ajoute à la ligne suivante
                }
            } else {
                this.latextArea.elements.push([new NewLineElement(this.latextArea)]);
                this.latextArea.elements.push([new TextElement(this.latextArea, str2)]);
                this.latextArea.parent.appendChild(latextArea.elements[i + 1][0].DOM);
                this.latextArea.parent.appendChild(latextArea.elements[i + 2][0].DOM);
            }
            if (elementCoupe instanceof InputElement) {
                if (elementCoupe.iCurseur > str1.length) {
                    elementCoupe.toTextElement();
                    elementCoupe.latextArea.elements[i + 2][0].toInput(elementCoupe.iCurseur - elementCoupe.curseur - 1);
                } else {
                    elementCoupe.DOM.setSelectionRange(elementCoupe.iCurseur, elementCoupe.iCurseur);

                }
            }
            this.setSize();
            width += elementCoupe.DOM.offsetWidth;
        }
        if (this.latextArea.elements.length >= i + 2) {
            this.latextArea.elements[i + 2][0].resizeForward();
        }
    }

    resizeBackward() {
        var compteur = 0;
        //this.DOM.style.height = '1em';
        this.setSize();
        var i = this.latextArea.findIndexes(this)[0];
        var width = this.latextArea.elements[0][0].DOM.offsetLeft;
        for (let element of this.latextArea.elements[i]) {
            width += element.DOM.offsetWidth;
        }
        var parentWidth = this.DOM.parentElement.offsetWidth;
        var change = false;
        while ((!change) && (this.latextArea.elements.length > i + 2) && !(this.latextArea.elements[i + 1][0].lineBreak)) {  // resize backward
            if (compteur == 100) { break; }
            compteur++;
            let elementAjout = this.latextArea.elements[i][this.latextArea.elements[i].length - 1];
            let elements = this.latextArea.elements;
            let elementCoupe;
            var k = 0;
            while ((elementCoupe == undefined) && (k < elements[i + 2].length)) { // On cherche le premier element de la ligne avec du texte
                if (elements[i + 2][k].text.length > 0) {
                    elementCoupe = elements[i + 2][k];
                }
                k++;
            }
            if (elementCoupe != undefined) {    // Il y a quelque chose sur la ligne suivante
                var positionPremierMot = elementCoupe.text.indexOf(' ');
                if ((positionPremierMot == -1) || (elementCoupe instanceof MathElement)) {
                    positionPremierMot = elementCoupe.text.length;
                }
                var str1 = ' ' + elementCoupe.text.substring(0, positionPremierMot);
                var str2 = elementCoupe.text.substring(positionPremierMot + 1);
                width -= elementAjout.DOM.offsetWidth;
                elementAjout.setText(elementAjout.text + str1);
                elementAjout.setSize();
                width += elementAjout.DOM.offsetWidth;
                if (width > parentWidth) {       // on vérifie que ça ne dépasse pas 
                    change = true; // sinon on enlève ce qu'on a fait
                    elementAjout.setText(elementAjout.text.substring(0, elementAjout.text.length - positionPremierMot - 1));
                } else {
                    elementCoupe.setText(str2);
                    if (elementCoupe instanceof InputElement) {
                        let posCurseur = elementCoupe.curseur;
                        elementCoupe.toTextElement();
                        elementAjout.toInput(elementAjout.text.length - positionPremierMot + posCurseur);
                    }
                }
            } else {
                change = true;
            }
            elementAjout.setSize();
        }
        if (this.latextArea.elements.length >= i + 2) {
            this.latextArea.elements[i + 2][0].resizeBackward();
        }
    }

    setSize() {
        this.DOM.style.height = this.DOM.scrollHeight + "px";
        this.DOM.style.width = '1px';
        this.DOM.style.width = this.DOM.scrollWidth + "px";
    }

    setText(str) {
        this.textContent = str;
        this.DOM.innerHTML = str.replace(/ /g, "&nbsp;");;
    }
}


class AudioResponseElement extends LatextAreaElement {

    constructor(latextArea, choices, token, maxElements = 8) {
        super(latextArea, '');
        this.maxElements = maxElements;
        this.token = token;
        this.updateChoices(choices, token);
    }

    build() {
        let DOM = document.createElement('div');
        DOM.className = "audio-choice";
        for (let i = 0; i < this.choices.length && i < this.maxElements; i++) {
            let span = document.createElement('span');
            span.onclick = () => {
                this.choose(this.choices[i]);

                let cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
                let formData = new FormData;
                let request = new XMLHttpRequest();

                request.open("POST", validateChoiceLink);
                request.setRequestHeader("X-CSRFToken", cSRFToken)

                formData.append('token', this.token);
                formData.append('document', docID);
                formData.append('choice', i);

                request.send(formData);
                this.destroy();
            };
            span.innerHTML = this.choices[i];
            DOM.appendChild(span);
            DOM.appendChild(document.createElement('br'));
        }
        DOM.style.position = "absolute";
        if (this.latextArea.editionMode == 1) {
            let rect = this.latextArea.activeElement.DOM.getBoundingClientRect();
            DOM.style.top = (rect.top + rect.height) + "px";
            DOM.style.left = (rect.left) + "px";
        }
        else if (this.latextArea.editionMode == 2) {
            let rect = this.latextArea.DOM.getBoundingClientRect();
            DOM.style.bottom = (rect.height) + "px";
            DOM.style.left = (rect.left) + "px";
        }
        try {
            this.DOM.remove();
        }
        catch (error) { }
        this.DOM = DOM;
        document.body.appendChild(this.DOM);
    }

    choose(choice) {
        if (this.latextArea.editionMode == 1) { 
            this.latextArea.activeElement.insert(choice);
        }
        if (this.latextArea.editionMode == 2) {
            insertAtCursor(choice, this.latextArea.DOM);
        }

        this.latextArea.choiceHappened = true;
        document.getElementById("start_rec").onclick = () => {
            sendContinuousAudio(500, voiceAnalysisLink, true, this.latextArea.audioResponseManager);
        };
        document.getElementById("start_rec").style.display = "inline-block";
    }

    destroy() {
        this.DOM.remove();
        this.latextArea.audioResponseManager = undefined;
        this.latextArea.killNextAudio = true;
        document.getElementById("stop_rec").click();
    }

    updateChoices(choices, token) {
        this.choices = choices;
        this.token = token;
        this.build();
    }

}


class EmptyElement extends LatextAreaElement {

    constructor(latextArea) {
        super(latextArea, '', 0);
        this.DOM = document.createElement('span');
        this.DOM.innerHTML = "";
    }
}


class InputElement extends LatextAreaElement {

    constructor(latextArea, text, position) {
        // initialisation
        super(latextArea, text, position);
        this.DOM = document.createElement("textArea");
        this.DOM.value = text;
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

    get curseur() {
        return this.DOM.selectionEnd;
    }

    insert(value) {
        if (this.DOM.value != "" && this.DOM.value.substr(this.DOM.value.length - 1) != " ") {
            value = " " + value;
        }
        this.DOM.value += value;
        this.latextArea.manageChange();
    }

    setText(str) {
        var curseur = this.curseur;
        this.textContent = str;
        this.DOM.value = str;
        this.DOM.setSelectionRange(curseur, curseur);
    }

    resize() {
        this.resizeForward();
        var i = Math.max(0, this.latextArea.findIndexes(this)[0] - 2);
        this.latextArea.elements[i][0].resizeBackward();

        //this.latextArea.elements[i][0].resizeBackward1();
        //this.resizeBackward1();
        //this.resizeBackward2();
    }

    toTextElement() {
        if (this.DOM.value.indexOf('\n') == -1) {
            var patt = /(\$\$[^\$]*\$\$|\$[^\$]*\$)/g;
            let text = this.DOM.value.replace(patt, "{breaK}$&{breaK}");
            let contentText = text.split(/\{breaK\}/);
            let newElements = [];
            let curseur = 0;
            this.iCurseur = this.curseur;
            for (let elem of contentText) {
                curseur = 0;
                if (this.iCurseur <= elem.length) {
                    curseur = this.iCurseur;
                } else {
                    this.iCurseur -= elem.length;
                }
                if (elem[0] == '\$') {
                    let textElement = new MathElement(this.latextArea, elem, curseur);
                    newElements.push(textElement);
                } else {
                    if (elem.length > 0) {
                        let textElement = new TextElement(this.latextArea, elem, curseur);
                        newElements.push(textElement);
                    }
                }
            }
            this.latextArea.replaceElement(this, newElements);
        }
        /*else {
            let values = this.DOM.value.split('\n');
            let elements = [];
            for (let value of values) {
                elements.push(new TextElement(this.latextArea, value));
                elements.push(new NewLineElement(this.latextArea));
            }
            if (elements.length != 0)
            elements.pop();
            this.latextArea.replaceElement(this, elements);
        }*/
        MathJax.Hub.Typeset();
    }

    toInput(positionFocus) {
        if (positionFocus != undefined) {
            var curseur = positionFocus;
        } else {
            var curseur = this.curseur;
        }
        this.DOM.setSelectionRange(curseur, curseur);
    }

    mouvementHandler(event) {
        var i = this.latextArea.findIndexes(this)[0];
        var j = this.latextArea.findIndexes(this)[1];
        var positionCurseur = this.curseur;
        var positionCurseurLine = this.curseurLigne;
        var longueur = this.DOM.value.length;
        var nbLines = (this.DOM.value.match(/\n/g) || []).length + 1;
        var currentLine = -1 * ((this.DOM.value.substring(positionCurseur).match(/\n/g) || []).length - nbLines);

        var iToFocus = i;
        var jToFocus = j;
        var positionFocus = 0;
        var change = false;
        var merge = false;
        // Gestion des touches (à réorganiser en switch à la fin)
        if (event.keyCode == 37 && positionCurseur == 0) {                //flèche gauche
            if (j > 0) {
                jToFocus = j - 1;
                positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length - 1;
                change = true;
            }
            else if (i > 0) {
                iToFocus = i - 2;
                jToFocus = this.latextArea.elements[iToFocus].length - 1;
                positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length;
                change = true;
            }
        }
        if (event.keyCode == 39 && positionCurseur - longueur == 0) {           //flèche droite
            if (j < this.latextArea.elements[iToFocus].length - 1) {
                jToFocus = j + 1;
                positionFocus = 1;
                change = true;
            }
            else if (i < this.latextArea.elements.length - 2) {
                iToFocus = i + 2;
                jToFocus = 0;
                change = true;
            }
        }
        if (event.keyCode == 38 && currentLine == 1) {                        //flèche haut
            if (i > 0) {
                iToFocus = i - 2;
                jToFocus = 0;
                change = true;
                while (this.latextArea.elements[iToFocus][jToFocus].text.length < positionCurseurLine) {
                    positionCurseurLine -= this.latextArea.elements[iToFocus][jToFocus].text.length;
                    if (jToFocus < this.latextArea.elements[iToFocus].length - 1) jToFocus++;
                }
                positionFocus = positionCurseurLine;
            }
        }
        if (event.keyCode == 40 && currentLine == nbLines) {                  //flèche bas
            if (i < this.latextArea.elements.length - 2) {
                iToFocus = i + 2;
                jToFocus = 0;
                change = true;
                while (this.latextArea.elements[iToFocus][jToFocus].text.length < positionCurseurLine) {
                    positionCurseurLine -= this.latextArea.elements[iToFocus][jToFocus].text.length;
                    if (jToFocus < this.latextArea.elements[iToFocus].length - 1) jToFocus++;
                }
                positionFocus = positionCurseurLine;
            }
        }

        if (change) {
            this.toTextElement();
            //setTimeout(0);
            this.latextArea.elements[iToFocus][jToFocus].toInput(positionFocus);
        }

        if (event.keyCode == 8) {
            if (positionCurseur == 0) {                   //backspace
                event.preventDefault();
                if (j > 0) {
                    jToFocus = j - 1;
                    merge = true;
                }
                else if (i > 0) {
                    iToFocus = i - 2;
                    jToFocus = this.latextArea.elements[iToFocus].length - 1;
                    merge = true;
                }
            }
        }
        if (merge) {
            positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length;
            this.latextArea.merge(this.latextArea.elements[iToFocus][jToFocus], this.latextArea.elements[i][j]);
            this.latextArea.elements[iToFocus][jToFocus].toInput(positionFocus);
        }
        if (event.keyCode == 13) {                   //enter
            event.preventDefault();
            let newFirst = [];
            let newSecond = [];
            for (let k = 0; k < j; k++) newFirst.push(this.latextArea.elements[i][k]);
            newFirst.push(new TextElement(this.latextArea, this.DOM.value.substring(0, positionCurseur)));
            let newLine = [new NewLineElement(this.latextArea, true)];
            newSecond.push(new TextElement(this.latextArea, this.DOM.value.substring(positionCurseur)));
            for (let k = j + 1; k < this.latextArea.elements[i].length; k++) newSecond.push(this.latextArea.elements[i][k]);
            this.latextArea.replaceLine(this.latextArea.elements[i], [newFirst, newLine, newSecond]);
            this.latextArea.elements[i + 2][0].toInput();
        }
    }

}


class NewLineElement extends LatextAreaElement {

    constructor(latextArea, lineBreak) {
        super(latextArea, '\n');
        if (lineBreak != undefined) {
            this.lineBreak = lineBreak;
        } else {
            this.lineBreak = false;
        }
        this.DOM = document.createElement('br');
    }

    toInput() {
        let newElement = new InputElement(this.latextArea, '\n');
        this.latextArea.replaceElement(this, newElement);
    }

}


class TextElement extends LatextAreaElement {

    constructor(latextArea, text, position) {
        // initialisation
        if (position == undefined)
            position = 0;
        super(latextArea, text, position);
        this.DOM = document.createElement("span");
        this.DOM.innerHTML = text.replace(/ /g, "&nbsp;");
        this.DOM.className = "latext-element";

        // event bindings
        this.DOM.onclick = this.toInput.bind(this, this.iCurseur);
    }

    insert(value) {
        if (this.DOM.innerText != "" && this.DOM.innerText.substr(this.DOM.innerText.length - 1) != " ") {
            value = " " + value;
        }
        this.DOM.innerText += value;
        this.textContent += value;
        this.latextArea.manageChange();
    }

    toInput(positionFocus) {
        if (positionFocus != undefined) {
            var curseur = positionFocus;
        } else {
            var curseur = this.curseur;
        }
        let newElement = new InputElement(this.latextArea, this.textContent, curseur);
	this.latextArea.replaceElement(this, newElement);
        newElement.DOM.setSelectionRange(curseur, curseur);
    }

}


class MathElement extends LatextAreaElement {

    constructor(latextArea, text, position) {
        // initialisation
        super(latextArea, text, position);
        this.DOM = document.createElement("span");
        this.DOM.innerHTML = text.replace(/ /g, "&nbsp;");
        this.DOM.className = "latext-element";
        // event bindings
        this.DOM.onclick = this.toInput.bind(this, this.iCurseur);
    }

    insert(value) {
        if (this.DOM.innerText != "" && this.DOM.innerText.substr(this.DOM.innerText.length - 1) != " ") {
            value = " " + value;
        }
        this.DOM.innerText += value;
        this.textContent += value;
        this.latextArea.manageChange();
    }

    toInput(positionFocus) {
        if (positionFocus != undefined) {
            var curseur = positionFocus;
        } else {
            var curseur = this.curseur;
        }
        let newElement = new InputElement(this.latextArea, this.textContent, curseur);
        newElement.DOM.setSelectionRange(curseur, curseur);
        this.latextArea.replaceElement(this, newElement);
    }

}
