function useAudioBlobs(blobManager, manageButtons = false, maxLength = 0) {
	if (navigator.mediaDevices) {
		var mediaRecorder = undefined;
		navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
			var audioCtx = new AudioContext();
			var dest = audioCtx.createMediaStreamDestination();
			mediaRecorder = new MediaRecorder(dest.stream);
			var source = audioCtx.createMediaStreamSource(stream);
			var manualStop = false;

			// Permet la gestion de l'affichage des boutons
			if (manageButtons) {
				document.getElementById("start_rec").style.display = "none";
				document.getElementById("stop_rec").style.display = 'inline-block';
			}
			
			// Permet d'arrêter l'enregistrement par boutton
			document.getElementById("stop_rec").onclick = function () {
				try {
					latextArea.stopDisplayingAudioChoices();
				}
				catch {}
				mediaRecorder.stop();
				manualStop = true;
				if (manageButtons) {
					document.getElementById("start_rec").style.display = "inline-block";
					document.getElementById("stop_rec").style.display = 'none';
				}
			};

			// On permet la concatenation des données audio
			mediaRecorder.ondataavailable = function (evt) {
				chunks.push(evt.data);
			};

			// On lance la captation de l'audio
			source.connect(dest);
			mediaRecorder.start();

			if (maxLength != 0) {
				setTimeout(function(){
					mediaRecorder.stop();
				}, maxLength);
			}

			stoppedRecorderManager = function (evt) {
				var blob = new Blob(chunks, { 'type': 'audio/ogg' });
				if (manageButtons && manualStop) {
					document.getElementById("stop_rec").style.display = 'none';
				}			
				blobManager(blob);
				if (maxLength && !manualStop) {
					mediaRecorder.start();
					setTimeout(function(){
						try {
							mediaRecorder.stop();
						}
						catch (error) {}
					}, maxLength);
					mediaRecorder.onstop = stoppedRecorderManager;
				}
				else {
					stream.stop();
				}
			};
			mediaRecorder.onstop = () => {
				stoppedRecorderManager();
			}
		});
		return mediaRecorder;
	}
	else {
		return(undefined);
	}
}

function sendAudioBlob(link, manageButtons, responseManager, additionalData = undefined) {
	// On prépare une requête contenant le fichier audio dans un blob audio
	var request = new XMLHttpRequest();
	var formData = new FormData;
	var cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
	formData.append("additionalData", additionalData);
	request.open("POST", link);
	request.setRequestHeader("X-CSRFToken", cSRFToken);
	useAudioBlobs(function(blob) {
		formData.append("file", blob);
		// On affiche le fait que l'on communique avec le serveur et on lance la requête
		communicationIndicatorManager.addRequest();
		request.send(formData);
	
		// On gère la réception de réponse
		request.onreadystatechange = function () {
			if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
				communicationIndicatorManager.endRequest();
				if (manageButtons) {
					document.getElementById("start_rec").style.display = "inline-block";
				}
				var response = JSON.parse(request.responseText);
				responseManager(response);
			}
		};
	}, manageButtons, 0);
}

function sendContinuousAudio(delay, link, manageButtons, responseManager) {
	chunks = [];
	return useAudioBlobs(function(blob){
		let request = new XMLHttpRequest();
		let formData = new FormData;
		let cSRFToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
		formData.append("additionalData", undefined);
		request.open("POST", link);
		request.setRequestHeader("X-CSRFToken", cSRFToken);
	        formData.append("file", blob);
	        formData.append('document', docID);
		// On affiche le fait que l'on communique avec le serveur et on lance la requête
		communicationIndicatorManager.addRequest();
		request.send(formData);
	
		// On gère la réception de réponse
		request.onreadystatechange = function () {
			if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
				communicationIndicatorManager.endRequest();
				let response = JSON.parse(request.responseText);
				responseManager(response);
			}
		};
	}
	, manageButtons, delay);
}

// TO DO : do this cleverly
var chunks = [];
