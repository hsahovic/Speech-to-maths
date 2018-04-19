// TO DO
//
// Dans manage change, rebrancher ce qui manque sur les états des autres classes
// Comment supprimer un saut de ligne
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

    get activeElement() {
        for (let line of this.elements) {
            for (let element of line) {
                if (element.DOM == document.activeElement) return element;
            }
        }
        for (let i = this.elements.length - 1; i >= 0; i--)
            for (let j = this.elements[i].length-1; j>=0; j--)
            if (this.elements[i][j] instanceof TextElement ||
                this.elements[i][j] instanceof InputElement)
                return this.elements[i][j];
    }

    get text() {
        let str = '';
        for (let line of this.elements) {
            for (let element of line)
                str += element.text;
        }
        return str;
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
            else
                this.audioResponseElement.updateChoices(response.content, response.token);
        }
    }

    generateDOM() {
        if (this.elements.length == 0) {
            this.elements.push([new TextElement(this, "")]);
        }
        for (let children of this.parent.children) {
            children.remove();
        }
        for (let line of this.elements) {
            for (let element of line)
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

    merge(firstElement, secondElement) {
        let iFirst = this.findIndexes(firstElement)[0];
        let jFirst = this.findIndexes(firstElement)[1];
        let iSecond = this.findIndexes(secondElement)[0];
        let jSecond = this.findIndexes(secondElement)[1];
        if (iFirst!= iSecond) {
            this.mergeLines(this.elements[iFirst], this.elements[iSecond]);
        }
        let start = this.elements.slice(0, iFirst);
        let end = this.elements.slice(iSecond + 1);

        let mergedElement = new TextElement(this, firstElement.text + secondElement.text);
        let tmpMerge = [];
        for (let j = 0; j < jFirst; j++) tmpMerge.push(this.elements[iFirst][j]);
        tmpMerge.push(mergedElement);
        for (let j = jFirst+2; j < this.elements[iFirst].length; j++) tmpMerge.push(this.elements[iFirst][j]);


        let tmpLine = [];
        this.elements = [];
        for (let line of start) {
            for (let element of line) tmpLine.push(element);
            this.elements.push(tmpLine);
            tmpLine = [];
        }
        this.elements.push(tmpMerge);
        for (let line of end) {
            for (let element of line) tmpLine.push(element);
            this.elements.push(tmpLine);
            tmpLine = [];
        }

        // un peu couteux, voir s'il n'y a pas plus simple
        firstElement.DOM.remove();
        secondElement.DOM.remove();
        this.generateDOM();
    }

    mergeLines(firstLine, secondLine) {
        let indexFirst = this.elements.indexOf(firstLine);
        let indexSecond = this.elements.indexOf(secondLine);
        let start = this.elements.slice(0, indexFirst + 1);
        let end = this.elements.slice(indexSecond + 1);
        let tmpLine = [];

        this.elements = [];
        for (let line of start) {
            for (let element of line) tmpLine.push(element);
            this.elements.push(tmpLine);
            tmpLine = [];
        }
        for (let element of secondLine) this.elements[indexFirst].push(element)
        for (let line of end) {
            for (let element of line) tmpLine.push(element);
            this.elements.push(tmpLine);
            tmpLine = [];
        }
        for (let element of firstLine) element.DOM.remove();
        for (let element of secondLine) element.DOM.remove();
        this.generateDOM();
    }

    parse() {
        let contentByLine = this.textContent.split(/\n/);
        for (let line of contentByLine) {
            line = line.replace(/\$(.*)\$/, "{breaK}$&{breaK}");
            let contentLine = line.split(/\{breaK\}/);
            let textLine = [];
            for (let elem of contentLine) {
                let textElement = new TextElement(this, elem);
                textLine.push(textElement);
            }
            this.elements.push(textLine);
            this.elements.push([new NewLineElement(this)]);
        }
        if (this.elements.length != 0)
            this.elements.pop();
        this.elements[0][0].toInput();
    }

    replaceElement(elementToReplace, newElements = undefined) {
        /*
            Replaces elementToReplace in this.elements
            newElements can be either :
                - undefined : in this case, elementsToReplace will just be deleted
                - an instance of LatextAreaElement
                - an array of instances of LatextAreaElement
        */

        let iToReplace = this.findIndexes(elementToReplace)[0];
        let jToReplace = this.findIndexes(elementToReplace)[1];
        let newLine = this.elements[iToReplace];
        let start = newLine.slice(0, jToReplace);
        let end = newLine.slice(jToReplace + 1);
        elementToReplace.DOM.remove();

        newLine = [];
        for (let element of start) newLine.push(element)
        if (newElements == undefined) {
            /* Nothing happens */
        }
        else if (newElements instanceof LatextAreaElement) {
            newLine.push(newElements);
        }
        else {
            for (let element of newElements) newLine.push(element);
        }
        for (let element of end) newLine.push(element);

        this.replaceLine(this.elements[iToReplace], newLine)

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

}


class AudioResponseElement extends LatextAreaElement {

    constructor(latextArea, choices, token, maxElements = 8) {
        super(latextArea, '');
        this.maxElements = maxElements;
        this.token = token;
        console.log(choices);
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
        let rect = this.latextArea.activeElement.DOM.getBoundingClientRect();
        DOM.style.top = (rect.top + rect.height) + "px";
        DOM.style.left = (rect.left) + "px";
        try {
            this.DOM.remove();
        }
        catch (error) { }
        this.DOM = DOM;
        document.body.appendChild(this.DOM);
    }

    choose(choice) {
        this.latextArea.activeElement.insert(choice);
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

    resize() {
        //this.DOM.style.height = '1em';
        this.DOM.style.height = this.DOM.scrollHeight + "px";
        this.DOM.style.width = '1px';
        this.DOM.style.width = this.DOM.scrollWidth + "px";
        var i = this.latextArea.findIndexes(this)[0];
        var width = this.latextArea.elements[0][0].DOM.offsetLeft;
        for (let element of this.latextArea.elements[i]) {
            width += element.DOM.offsetWidth;
        }

        while (width > this.DOM.parentElement.offsetWidth) {
            var l = this.latextArea.elements[i].length - 1;
            var elementCoupe = this.latextArea.elements[i][l];
            var positionDernierMot = Math.max(elementCoupe.text.lastIndexOf(' '), elementCoupe.text.lastIndexOf("&nbsp"));
            var str1 = elementCoupe.text.substring(0, positionDernierMot);
            var str2 = elementCoupe.text.substring(positionDernierMot + 1);
            width -= elementCoupe.DOM.offsetWidth;
            if (this==elementCoupe) {
                this.iCurseur = this.DOM.selectionEnd;
                this.DOM.value = str1;
            } else {
                elementCoupe.DOM.innerHTML = str1;
                elementCoupe.textContent = str1;
            }
            if (this.latextArea.elements.length>i+2) {
                this.latextArea.elements[i+2][0].textContent = str2 + ' ' + this.latextArea.elements[i+2][0].textContent;
                this.latextArea.elements[i+2][0].DOM.innerHTML = this.latextArea.elements[i+2][0].textContent.replace(/ /g, "&nbsp;");
            } else {
                this.latextArea.elements.push([new NewLineElement(this.latextArea)]);
                this.latextArea.elements.push([new TextElement(this.latextArea, str2)]);
                this.latextArea.parent.appendChild(latextArea.elements[i+1][0].DOM);
                this.latextArea.parent.appendChild(latextArea.elements[i+2][0].DOM);
            }
            if (this==elementCoupe) {
                if (this.iCurseur > str1.length) {
                    this.latextArea.elements[i+2][0].toInput(str2.length);    
                } else {
                    this.DOM.setSelectionRange(this.iCurseur, this.iCurseur);                
                }
            }
            this.DOM.style.height = this.DOM.scrollHeight + "px";
            this.DOM.style.width = '1px';
            this.DOM.style.width = this.DOM.scrollWidth + "px";
            width += elementCoupe.DOM.offsetWidth;
        }

        var change = false;
        while ( (!change) && (this.latextArea.elements.length>i+2) && (!this.latextArea.elements[i+1][0].lineBreak)) {
            var elementCoupe = this.latextArea.elements[i+2][0];
            var elementAjout = this.latextArea.elements[i][this.latextArea.elements[i].length-1];
            var positionPremierMot = elementCoupe.text.indexOf(' ');
            if (positionPremierMot != 0) {
                var str1 = elementCoupe.text.substring(0, positionPremierMot);
                var str2 = elementCoupe.text.substring(positionPremierMot + 1);
                width -= elementAjout.DOM.offsetWidth;
                if (elementAjout instanceof InputElement) {
                    elementAjout.iCurseur = this.DOM.selectionEnd;
                    elementAjout.DOM.value += ' ' + str1;
                    elementAjout.DOM.setSelectionRange(elementAjout.iCurseur, elementAjout.iCurseur);
                } else {
                    elementAjout.DOM.innerHTML += '&nbsp' + str1;
                    elementAjout.textContent += ' ' + str1;
                }
                this.DOM.style.height = this.DOM.scrollHeight + "px";
                this.DOM.style.width = '1px';
                this.DOM.style.width = this.DOM.scrollWidth + "px";
                width += elementAjout.DOM.offsetWidth;
                if (width <= this.DOM.parentElement.offsetWidth) {       // on vérifie que ça ne dépasse pas
                    elementCoupe.textContent = str2;
                    elementCoupe.DOM.innerHTML = str2;
                } else {
                    change = true;
                    if (elementAjout instanceof InputElement) {         // sinon on enlève ce qu'on a fait
                        elementAjout.iCurseur = elementAjout.curseur;
                        elementAjout.DOM.value = elementAjout.DOM.value.substring(0, elementAjout.text.length - positionPremierMot - 1);
                        elementAjout.DOM.setSelectionRange(elementAjout.iCurseur, elementAjout.iCurseur);
                    } else {
                        elementAjout.DOM.innerHTML = elementAjout.DOM.innerHTML.substring(0, elementAjout.DOM.innerHTML.length - positionPremierMot);
                        elementAjout.textContent = elementAjout.DOM.innerHTML.replace(/&nbsp;/g, " ");
                    }
                }
            } else {
                change = true;
            }
            
            this.DOM.style.height = this.DOM.scrollHeight + "px";
            this.DOM.style.width = '1px';
            this.DOM.style.width = this.DOM.scrollWidth + "px";        
        }
    }

    toTextElement() {
        if (this.DOM.value.indexOf('\n') == -1) {
            this.latextArea.replaceElement(this, new TextElement(this.latextArea, this.DOM.value, this.curseur));
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

    mouvementHandler(event) {
        var i = this.latextArea.findIndexes(this)[0];
        var j = this.latextArea.findIndexes(this)[1];
        var positionCurseur = this.curseur;
        var positionCurseurLine = this.curseurLigne;
        var longueur = this.DOM.value.length;
        var nbLines = (this.DOM.value.match(/\n/g) || []).length + 1;
        var currentLine = -1* ((this.DOM.value.substring(positionCurseur).match(/\n/g) || []).length - nbLines);

        var iToFocus = i;
        var jToFocus = j;
        var positionFocus = 0;
        var change = false;
        var merge = false;
        // Gestion des touches (à réorganiser en switch à la fin)
        if (event.keyCode == 37 && positionCurseur == 0) {                //flèche gauche
            if (j > 0) {
                jToFocus = j-1;
                positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length-1;
                change = true;
            } 
            else if (i>0) {
                iToFocus = i-2;
                jToFocus = this.latextArea.elements[iToFocus].length-1;
                positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length;
                change = true;
            }
        }
        if (event.keyCode == 39 && positionCurseur - longueur == 0) {           //flèche droite
            if (j < this.latextArea.elements[iToFocus].length-1) {
                jToFocus = j+1;
                positionFocus = 1;
                change = true;
            } 
            else if (i < this.latextArea.elements.length-2) {
                iToFocus = i+2;
                jToFocus = 0;
                change = true;
            }
        }
        if (event.keyCode == 38 && currentLine == 1) {                        //flèche haut
            if (i > 0) {
                iToFocus = i-2;
                jToFocus = 0;
                change = true;
                while (this.latextArea.elements[iToFocus][jToFocus].text.length < positionCurseurLine) {
                    positionCurseurLine -= this.latextArea.elements[iToFocus][jToFocus].text.length;
                    if (jToFocus < this.latextArea.elements[iToFocus].length-1) jToFocus++;
                }
                positionFocus = positionCurseurLine;
            } 
        }
        if (event.keyCode == 40 && currentLine == nbLines) {                  //flèche bas
            if (i < this.latextArea.elements.length - 2) {
                iToFocus = i+2;
                jToFocus = 0;
                change = true;
                while (this.latextArea.elements[iToFocus][jToFocus].text.length < positionCurseurLine) {
                    positionCurseurLine -= this.latextArea.elements[iToFocus][jToFocus].text.length;
                    if (jToFocus < this.latextArea.elements[iToFocus].length-1) jToFocus++;
                }
                positionFocus = positionCurseurLine;
            } 
        }

        if (change) {
                this.latextArea.elements[iToFocus][jToFocus].toInput(positionFocus);
                this.toTextElement();
        }

        if (event.keyCode == 8 && positionCurseur == 0) {                   //backspace
            event.preventDefault();
            if (j > 0) {
                jToFocus = j-1;
                merge = true;
            } 
            else if (i>0) {
                iToFocus = i-2;
                jToFocus = this.latextArea.elements[iToFocus].length-1;
                merge = true;
            }
        }
        if (merge) {
                positionFocus = this.latextArea.elements[iToFocus][jToFocus].textContent.length;
                this.latextArea.merge(this.latextArea.elements[iToFocus][jToFocus], this.latextArea.elements[i][j]);
                this.latextArea.elements[iToFocus][jToFocus].toInput(positionFocus);
        }
        if (event.keyCode == 13 ) {                   //enter
            event.preventDefault();
            let newFirst = [];
            let newSecond = [];
            for (let k=0; k<j; k++) newFirst.push(this.latextArea.elements[i][k]);
            newFirst.push(new TextElement(this.latextArea, this.DOM.value.substring(0, positionCurseur) ));
            let newLine = [new NewLineElement(this.latextArea, true)];
            newSecond.push(new TextElement(this.latextArea, this.DOM.value.substring(positionCurseur) ));
            for (let k=j+1; k<this.latextArea.elements[i].length; k++) newSecond.push(this.latextArea.elements[i][k]);
            this.latextArea.replaceLine(this.latextArea.elements[i], [newFirst, newLine, newSecond]);
            this.latextArea.elements[i+2][0].toInput();
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
