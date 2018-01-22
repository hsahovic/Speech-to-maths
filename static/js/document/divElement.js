class divElement {

    constructor(text) {
        this.listeElement = parse(txt);
    }

}



function parse(txt) {
    var arr = new Array();
    str = str.replace( /\r?\n/g, "<br>" );
    arr = str.split(/\<br\>|\<br \/\>/);

    var res = new Array();
    for (i = 0; i < arr.length; i++) {
        if (arr[i].indexOf('\$')>=0) {
            var element = new ElementMatjax(arr[i], i); 
        }
        else {
            var element = new ElementHTML(arr[i], i);             
        } 
        res.push(element);
    }
}



// Affiche/cache la preview en MathJax et Cache/affiche la zone de saisie

function preview(div1, divtext, id)
{
    var arr = new Array();
    var div = document.getElementById(div1);
    var divt = document.getElementById(divtext);
    var text = document.getElementById(divtext).value;
    arr = getValText(text);
    /*
    document.getElementById(divtext).innerHTML = str;
    if(document.getElementById(div1).style.display=="none")
    {
        document.getElementById(div1).style.display="block";
        document.getElementById(divtext).style.display="none";
    }
    else
    {
        document.getElementById(div1).style.display="none";
        document.getElementById(divtext).style.display="block";
    }*/  
    div.innerHTML = "";
    changeVisible(arr, id);
    for (i = 0; i < arr.length; i++) {
        div.innerHTML += arr[i].toStringAffiche() + "<br>"; 
    }
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    return true;
}

function ecrireTxt(div1, str, id) {
    var arr = new Array();
    var div = document.getElementById(div1);
    arr = getValText(str);
    div.innerHTML = "";
    changeVisible(arr, id);
    for (i = 0; i < arr.length; i++) {
        div.innerHTML += arr[i].toStringAffiche() + "<br>"; 
    }
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    return true;
}


// Gère le contenu à afficher dans la div pour MathJax
function getValText(str)
{
    var arr = new Array();
    str = str.replace( /\r?\n/g, "<br>" );
    arr = str.split(/\<br\>|\<br \/\>/);

    var res = new Array();
    for (i = 0; i < arr.length; i++) {
        if (arr[i].indexOf('\$')>=0) {
            var element = new ElementMatjax(arr[i], i); 
        }
        else {
            var element = new ElementHTML(arr[i], i);             
        } 
        res.push(element);
    }
    str = str.replace("\\begin{center}", "<span style='text-align:center'>").replace("\\end{center}", "</span>");
    str = str.replace("\\begin{flushleft}", "<span>").replace("\\end{flushleft}", "</span>");
    str = str.replace("\\begin{flushright}", "<span style='float:right'>").replace("\\end{flushright}", "</span>");
    str = str.replace("\\begin{document}", "<span>\\begin{</span><span class='additional-data' style='font-weight:bold'>document</span>}").replace("\\end{document}", "<span>\\end{</span><span class='additional-data' style='font-weight:bold'>document</span>}");
    return res;
}


function changeVisible(arr, id) {
    res = resetVisible(arr);
    res[id].visible= false;
    return res;
}

function resetVisible(arr) {
    for (i = 0; i < arr.length; i++) {
        arr[i].visible = true;
    }
    return arr;
}

