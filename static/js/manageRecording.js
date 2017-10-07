function manageRecording(link, manageResponse) {
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
				request.open("POST", link);
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
					        manageResponse(response);
						document.getElementById("start_rec").style.display = "inline-block";
						stream.stop();
					}
				};
			};
		});
	}
}
