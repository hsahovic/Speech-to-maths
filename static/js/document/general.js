function audioResponseManager (response) {
	if (response.instruction == "write") {
		insertAtCursor(response.content[0], document.getElementsByName('content')[0]);
	}
}

function manageContentChange(ajaxDelay) {
	// Gère la modification du contenu ; 
	// Permet de donner une valeur par défaut à ajaxDelay

	if (ajaxDelay == undefined) {
		ajaxDelay = .5;
	}
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
            var data = { "docID": docID, "newContent": document.getElementsByName("content")[0].value };
            contentStateManager.newState(data.newContent);
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


function manageQueueButtonsStyle () {
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
        case "ArrowDown" :
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

function preview(id1, id2, id3)
{
    var str = "getValText(id3)";
    document.getElementById(id2).innerHTML = str;
    if(document.getElementById(id1).style.display=="none")
    {
        document.getElementById(id1).style.display="block";
        document.getElementById(id2).style.display="none";
    }
    else
    {
        document.getElementById(id1).style.display="none";
        document.getElementById(id2).style.display="block";
    }
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    return true;
}
// Gère le contenu à afficher dans la div en MathJax
function getValText(id)
{
    var str = document.getElementById(id).value;
    str = str.replace( /\r?\n/g, "<br>" );
    str = str.replace("\\begin{center}", "<span style='text-align:center'>").replace("\\end{center}", "</span>");
    str = str.replace("\\begin{flushleft}", "<span>").replace("\\end{flushleft}", "</span>");
    str = str.replace("\\begin{flushright}", "<span style='float:right'>").replace("\\end{flushright}", "</span>");
    str = str.replace("\\begin{document}", "<span>\\begin{</span><span class='additional-data' style='font-weight:bold'>document</span>}").replace("\\end{document}", "<span>\\end{</span><span class='additional-data' style='font-weight:bold'>document</span>}");
    return str;
}

var changeHappened = false;
var contentStateManager = new ContentStateManager(document.getElementsByName('content')[0]);
manageQueueButtonsStyle();