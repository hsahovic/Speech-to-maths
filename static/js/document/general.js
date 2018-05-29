function audioResponseManager(response) {
    if (response.instruction == "write") {
        insertAtCursor(response.content[0], document.getElementsByName('content')[0]);
    }
}

function manageContentChange(ajaxDelay = .5) {
    // Gère la modification du contenu ; 

    if (changeHappened); // Si le changement est déjà pris en compte, on ne fait rien
    else { // Sinon, on indique qu'il est pris en compte et on programme une requête de maj pour le serveur
        changeHappened = true;

        var cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        var formData = new FormData;
        var request = new XMLHttpRequest();

        request.open("POST", documentSaveLink);
        request.setRequestHeader("X-CSRFToken", cSRFToken)

        setTimeout(function () {
            communicationIndicatorManager.addRequest();
            changeHappened = false;
            var data = { "docID": docID, "newContent": latextArea.text };
            // contentStateManager.newState(data.newContent);
            data = JSON.stringify(data);
            formData.append("data", data);
            request.send(formData);
            request.onreadystatechange = function () {
                if (request.readyState == 4 && request.status == 200) {
                    communicationIndicatorManager.endRequest();
                }
            }
            manageQueueButtonsStyle();
        }, 1000 * ajaxDelay);
    }
}


function manageQueueButtonsStyle() {
    // Gestion de l'apparence des boutons en avant / en arrière
    if (contentStateManager.isOnLastState()) {
        if (document.getElementById("moveForward").className.search(" disabled") == -1) {
            document.getElementById("moveForward").className += " disabled";
            document.getElementById("moveForward").disabled = true;
        }
    }
    else {
        document.getElementById("moveForward").className = document.getElementById("moveForward").className.replace(" disabled", "");
        document.getElementById("moveForward").disabled = false;
    }
    if (contentStateManager.isOnFirstState()) {
        if (document.getElementById("moveBackward").className.search(" disabled") == -1) {
            document.getElementById("moveBackward").className += " disabled";
            document.getElementById("moveBackward").disabled = true;
        }
    }
    else {
        document.getElementById("moveBackward").className = document.getElementById("moveBackward").className.replace(" disabled", "");
        document.getElementById("moveBackward").disabled = false;
    }
}


// On gère les raccourcis clavier
window.addEventListener("keydown", function (event) {
    if (event.defaultPrevented) {
        return; // Should do nothing if the key event was already consumed.
    }
    if (event.ctrlKey) {
        switch (event.key) {
            case "z":
                contentStateManager.moveBackward();
                manageQueueButtonsStyle();
                break;
            case "y":
                contentStateManager.moveForward();
                manageQueueButtonsStyle();
                break;
            case "l":
                addEnvironnement('flushleft');
                break;
            case "e":
                addEnvironnement('center');
                break;
            case "r":
                addEnvironnement('right');
                break;
            case "j":
                addEnvironnement('work in progress');
                break;
            case "Up":
            case "ArrowUp":
                sciptElement('exponent');
                break;
            case "ArrowDown":
            case "Down":
                sciptElement('subscript');
                break;
            default:
                return;
        }
    }

    // Consume the event for suppressing "double action".
    // event.preventDefault();
}, true);


// Affiche/cache la preview en MathJax et Cache/affiche la zone de saisie

function preview(id1, id2, id3) {
    var str = getValText(id3);
    document.getElementById(id2).innerHTML = str;
    if (document.getElementById(id1).style.display == "none") {
        document.getElementById(id1).style.display = "block";
        document.getElementById(id2).style.display = "none";
    }
    else {
        document.getElementById(id1).style.display = "none";
        document.getElementById(id2).style.display = "block";
    }
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    return true;
}
// Gère le contenu à afficher dans la div pour MathJax
function getValText(id) {
    var str = document.getElementById(id).value;
    str = str.replace(/\r?\n/g, "<br>");
    str = str.replace("\\begin{center}", "<span style='text-align:center'>").replace("\\end{center}", "</span>");
    str = str.replace("\\begin{flushleft}", "<span>").replace("\\end{flushleft}", "</span>");
    str = str.replace("\\begin{flushright}", "<span style='float:right'>").replace("\\end{flushright}", "</span>");
    str = str.replace("\\begin{document}", "<span>\\begin{</span><span class='additional-data' style='font-weight:bold'>document</span>}").replace("\\end{document}", "<span>\\end{</span><span class='additional-data' style='font-weight:bold'>document</span>}");
    return str;
}

function startRecording() {
    var mediaRecorder = sendContinuousAudio(500, voiceAnalysisLink, true, audioContentManager.manageAJAXResponse);
}

function getHelp(id) {
    let parent = document.getElementById(id);
    let query = parent.value;
    let formData = new FormData;
    let request = new XMLHttpRequest();

    request.open("POST", helpLink);
    request.setRequestHeader("X-CSRFToken", document.querySelector("[name=csrfmiddlewaretoken]").value);
    communicationIndicatorManager.addRequest();
    formData.append("query", query);
    request.send(formData);
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            let response = JSON.parse(request.responseText);
            let DOM = document.createElement("div");
            
            oldDOM = document.getElementById("help-text-responses");
            if (oldDOM != null)
                document.getElementsByTagName('body')[0].removeChild(document.getElementById("help-text-responses"));
            
            communicationIndicatorManager.endRequest();

            DOM.id = "help-text-responses";
            DOM.style.position = "absolute";
            
            let setPositions = () => {
                DOM.style.width = (document.getElementById('help').getBoundingClientRect().width - 2) + "px";
                DOM.style.top = (document.getElementById('help').getBoundingClientRect().top + document.getElementById('help').getBoundingClientRect().height) + "px";
                DOM.style.left = document.getElementById('help').getBoundingClientRect().left + "px";
            }

            setPositions();
            window.onresize = setPositions;
            window.onclick = (event) => {
                if (!document.getElementById('help-text-responses').contains(event.target)) {
                    document.getElementsByTagName('body')[0].removeChild(document.getElementById("help-text-responses"));
                    window.onclick = undefined;
                }
            };

            for (element of response) {
                let div = document.createElement("div");

                let divHeader = document.createElement("h1");
                let divLatexExample = document.createElement("div");
                let divSpeechExample = document.createElement("div");
                let divSpeech = document.createElement("div");
                let divCodeExample = document.createElement("div");
                
                div.className = "help-text-container";
                divHeader.className = "help-text-header";
                divLatexExample.className  = "help-text-latex-example";
                divCodeExample.className  = "help-text-code-example";
                divSpeechExample.className  = "help-text-speech-example";
                divSpeech.className = "help-text-speech";

                divHeader.innerHTML = element.name;
                divLatexExample.innerHTML = 'Exemple : $$'  + element["example-latex"] + '$$';
                divCodeExample.innerHTML = 'écrit <span class = "raw-code">'  + element["example-latex"] + "</span>";
                divSpeechExample.innerHTML = 'prononcé «'  + element.example + '»'; ;
                divSpeech.innerHTML = '<strong> Commande </strong>:  «' + element.spelling + '»';

                div.appendChild(divHeader);
                div.appendChild(divSpeech);
                div.appendChild(document.createElement('br'));
                div.appendChild(divLatexExample);
                div.appendChild(divSpeechExample);
                div.appendChild(divCodeExample);

                DOM.appendChild(div);
            }
            document.getElementsByTagName('body')[0].append(DOM);
            MathJax.Hub.Queue(["Typeset",MathJax.Hub,"help-text-responses"]);
            setTimeout(setPositions,0);
        }
    }
}

function getPDF(id) {
    let parent = document.getElementById(id);
    let formData = new FormData;
    let request = new XMLHttpRequest();

    request.open("POST", regeneratePDFLink);
    request.setRequestHeader("X-CSRFToken", document.querySelector("[name=csrfmiddlewaretoken]").value);
    communicationIndicatorManager.addRequest();
    request.send(formData);
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            let response = JSON.parse(request.responseText);
            communicationIndicatorManager.endRequest();
            console.log(response);
            if (response.toDo == ("newLink")){
                parent.src = response.pdfUrl;
                return;
            }
        }
    }
}

var changeHappened = false;
// Reactivate this
// var contentStateManager = new ContentStateManager(document.getElementsByName('content')[0]);
// manageQueueButtonsStyle();
