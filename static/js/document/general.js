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


function manageRecording() {
	// Cette fonction permet de démarrer un enregistrement audio et de l'envoyer à l'issue sur le serveur
	// Gère l'affichage du bouton de démarrage audio
	// On vérifie qu'on a accès à un flux audio, et le cas échéant on le capte
	if (navigator.mediaDevices) {
		navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
			var audioCtx = new AudioContext();
			var chunks = [];
			var dest = audioCtx.createMediaStreamDestination();
			var mediaRecorder = new MediaRecorder(dest.stream);
			var source = audioCtx.createMediaStreamSource(stream);
			document.getElementById("start_rec").style.display = "none";
			// On permet l'arrêt de l'enregistrement
			document.getElementById("stop_rec").style.display = 'inline-block';

			// On crée l'event manager pour l'arrêt de l'enregistrement
			document.getElementById("stop_rec").onclick = function () {
				mediaRecorder.stop();
			};

			// On permet la contatenation des données audio
			mediaRecorder.ondataavailable = function (evt) {
				chunks.push(evt.data);
			};

			// On lance la captation de l'audio
			source.connect(dest);
			mediaRecorder.start();
			// On gère l'event manager de la fin de flux
			mediaRecorder.onstop = function (evt) {
				// On prépare une requête contenant le fichier audio dans un blob audio
				var request = new XMLHttpRequest();
				var formData = new FormData;
				var blob = new Blob(chunks, { 'type': 'audio/ogg' });
				var cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
				formData.append("file", blob);
				request.open("POST", voiceAnalysisLink);
				request.setRequestHeader("X-CSRFToken", cSRFToken);

				// On affiche le fait que l'on communique avec le serveur et on lance la requête
				communicationIndicatorManager.addRequest();
				request.send(formData);

				// On gère la réception de réponse
				request.onreadystatechange = function () {
					if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
						document.getElementById("stop_rec").style.display = 'none';
						communicationIndicatorManager.endRequest();
						var response = JSON.parse(request.responseText);
						if (response.instruction == "write") {
							insertAtCursor(document.getElementsByName('content')[0], response.content[0]);
							manageContentChange();
						}
						document.getElementById("start_rec").style.display = "inline-block";
						stream.stop();
					}
				};
			};
		});
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

var changeHappened = false;
var contentStateManager = new ContentStateManager(document.getElementsByName('content')[0]);
manageQueueButtonsStyle();