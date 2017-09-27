function addEnvironnement(environnement, field = document.getElementsByName('content')[0]) {
    var pos = extendSelectionToLines(field.selectionStart, field.selectionEnd, field);
    var text = "\\begin{" + environnement + '}\n' + field.value.substring(pos.start, pos.end) + '\n\\end{' + environnement + '}\n';
    insertAtCursor(text, field);
    manageContentChange();
}


function extendSelectionToLines(start, stop, field = document.getElementsByName('content')[0]) {
    // Permet d'étendre une selection en ajoutant le début et fin de ligne
    // Renvoie un objet contenant les nouvelles et anciennes position sous les noms start, end, oldStart et oldStop
    var lines = field.value.split("\n");
    var chars = 0; // Compte le nombre de chars parcourus
    var newStart = start;
    // On parcourt les lignes jusqu'à trouver les limites de lignes encadrant la selection
    for (i = 0; i < lines.length; i++) {
        if (chars <= start) newStart = chars;
        if (chars >= stop) break;
        chars += lines[i].length + 1;
    }
    field.selectionStart = newStart;
    field.selectionEnd = chars;
    return { "start": newStart, "end": chars, "oldStart": start, "oldStop": stop };
}


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


function listButton(type, field = document.getElementsByName('content')[0]) {
    var text = '\\item ';
    // Si on a une selection, on la listifie par ligne
    if (field.selectionStart || field.selectionEnd) {
        var pos = extendSelectionToLines(field.selectionStart, field.selectionEnd, field);
        startPos = pos.start;
        endPos = pos.end;
        var sel = field.value.substring(startPos, endPos).split('\n').filter(a => (a != ""));
        text += sel.join('\n\\item ');
    }
    else {
        pos = { "start ": field.value.length + 1, "end": field.value.length + 1 };
        field.value += '\n';
    }
    switch (type) {
        case "unordered":
            text = "\\begin{itemize}\n" + text + "\n\\end{itemize}\n"
            break;
        case "ordered":
            text = "\\begin{ordered}\n" + text + "\n\\end{ordered}\n"
            break;
    }
    field.value = field.value.substring(0, pos.start)
        + text
        + field.value.substring(pos.end, field.value.length);
    field.focus();
    field.selectionStart = pos.start;
    field.selectionEnd = pos.start + text.length;
    manageContentChange();
}


function sciptElement(type, field = document.getElementsByName('content')[0]) {
    // Gère l'ajout d'exposant / indice
    var start = field.selectionStart;
    var end = field.selectionEnd;
    var value = field.value.substring(start, end);
    switch (type) {
        case "subscript":
            value = "_{" + value + "}";
            break;
        case "exponent":
            value = "^{" + value + "}"
            break;
    }
    insertAtCursor(value, field);
    field.focus();
    // Selectionne le texte dans l'element
    if (start || end) {
        field.selectionStart = start + 2;
        field.selectionEnd = end + 2;
    }
    else {
        field.selectionStart = field.value.length - value.length + 2;
        field.selectionEnd = field.value.length - 1;
    }
    manageContentChange();
}