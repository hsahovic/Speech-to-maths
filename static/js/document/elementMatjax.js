class ElementDocument {

    constructor(txt, i) {
        this.visible = true;
        this.text = txt;
        this.id = i;
    }

}


/* Classe qui gère le contenu d'un élément HTML*/
class ElementHTML extends ElementDocument {

    toStringAffiche() {
        if (!this.visible) {
            var str = "<textarea autofocus='on' style='height:100%; background-color:#a0c4ff;'\" >" + this.text + "</textarea>";
            return str;
        }
        else {
            var str = "<span style='width:100%; background-color:red;' onclick=\"ecrireTxt('divmat', docTXT, " + this.id.toString() + ")\">" + this.text + "</span>";
            return str;
        }
    }

    
}

/* Classe qui gère le contenu d'un élément Mathjax*/
class ElementMatjax extends ElementDocument {

    toStringAffiche() {
        if (!this.visible) {
            var str = "<textarea autofocus='on' style='height:100%; background-color:#a0c4ff;'\" >" + this.text + "</textarea>";
            return str;
        }
        else {
            var str = "<span style='width:100%; background-color:red;' onclick=\"ecrireTxt('divmat', docTXT, " + this.id.toString() + ")\">" + this.text + "</span>";
            return str;
        }
    }

}