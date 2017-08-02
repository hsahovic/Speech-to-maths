if (navigator.mediaDevices) {
	navigator.mediaDevices.getUserMedia ({audio: true}).then(function(stream) {
		var audioCtx = new AudioContext();
		var chunks = [];
		var dest = audioCtx.createMediaStreamDestination();
		var mediaRecorder = new MediaRecorder(dest.stream);
		var source = audioCtx.createMediaStreamSource(stream);
		
		document.getElementById("stop_rec").onclick = function () {
			mediaRecorder.stop();
		};
		
		mediaRecorder.ondataavailable = function(evt) {
			chunks.push(evt.data);
		};
		
		source.connect(dest);
		mediaRecorder.start();
		
		mediaRecorder.onstop = function(evt) {
			var blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
			var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
			var formData = new FormData;
			var request = new XMLHttpRequest();
			
			request.onreadystatechange = function () {
				if(request.readyState === XMLHttpRequest.DONE && request.status === 200) {
					document.getElementById("stop_rec").style.display = 'none';
					alert(request.responseText);
				}
			};
			
			formData.append("file", blob);
			request.open("POST", voice_analysis_link);
			request.setRequestHeader("X-CSRFToken", csrftoken)
			request.send(formData);
		};
		
		document.getElementById("stop_rec").style.display = 'inline-block';
		
	})
	.catch(function(err) {});
} 