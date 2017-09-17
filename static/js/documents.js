function orderLines(typeOfOrdering) {
	// Cette fonction permet de classer les lignes de la table contenant les informations de nos documents, selon un critère : 0 correspond au titre, 1 à l'auteur, 2 à la date
	var lines = [].slice.call(document.getElementsByClassName("_document"));
	var table = document.getElementsByTagName("table")[0];
	var tableHead = table.getElementsByTagName("th");
	var icons = 0;

	// On classe les lignes selon l'ordre d'une fonction définie par une fonction définie à la volée
	lines.sort(function (a, b) {
		if (typeOfOrdering == 2) {
			// On gère en premier lieu le classement par Date
			// Les lignes contiennent un input caché contenant la date en un format numérique aisément exploitable : AAAA MM JJ
			vara = a.getElementsByTagName('input')[0].value.split(' ');
			varb = b.getElementsByTagName('input')[0].value.split(' ');
			for (i = 0; i < vara.length; i++) {
				if (parseInt(vara[i]) > parseInt(varb[i])) {
					return 1;
				}
				if (parseInt(vara[i]) < parseInt(varb[i])) {
					return -1;
				}
			}
			return -1;
		}
		// Sinon, on classe selon l'ordre alphabétique
		if (a.getElementsByTagName("td")[typeOfOrdering].textContent.toLowerCase() > b.getElementsByTagName("td")[typeOfOrdering].textContent.toLowerCase()) {
			return 1;
		}
		return -1;
	});

	// Gère l'affiche des icônes liées au classement des éléments
	icons = document.getElementsByClassName("_decoration");
	// On supprime les icônes déjà présentes
	for (var i = 0; i < icons.length; i++) {
		icons[i].remove();
	}
	// Si le dernier classement effectué correspond au classement actuel, on inverse l'ordre des lignes à afficher... Et on traite l'icône différement !
	if (currentTypeOfOrdering == typeOfOrdering) {
		lines.reverse();
		currentTypeOfOrdering = -1;
		tableHead[typeOfOrdering].innerHTML += "<i class='fa fa-arrow-up _decoration' aria-hidden='true'></i>";
	}
	else {
		currentTypeOfOrdering = typeOfOrdering;
		tableHead[typeOfOrdering].innerHTML += "<i class='fa fa-arrow-down _decoration' aria-hidden='true'></i>";
	}
	for (var i = 0; i < lines.length; i++) {
		table.appendChild(lines[i]);
	}
	return 0;
}

function searchDocuments() {
	// Cette fonction permet de gérer les recherches sur la page documents
	// On récupère le terme recherché
	var searchValue = document.getElementsByTagName("input")[0].value.toLowerCase()
	var lines = document.getElementsByClassName("_document");

	// On envoie une requête au serveur interrogeant le contenu des documents
	var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
	var formData = new FormData;
	var request = new XMLHttpRequest();
	request.open("POST", documentsSearchLink);
	request.setRequestHeader("X-CSRFToken", csrftoken)

	var data = { "searchValue": searchValue };
	data = JSON.stringify(data);
	formData.append("data", data);

	communicationIndicatorManager.addRequest();
	request.send(formData);

	// On effectue une recherche sur les contenus des lignes
	for (var i = 0; i < lines.length; i++) {
		if (lines[i].textContent.toLowerCase().indexOf(searchValue) >= 0) {
			lines[i].style.display = "table-row";
		}
		else {
			lines[i].style.display = "none";
		}
	}

	var spans = document.getElementsByClassName("_search_content");
	for (i = 0; i < spans.length; i++) {
		spans[i].innerHTML = "";
	}

	// Une fois la recherche effectuée, et une fois notre requête receptionnée en bonne et due forme, on affiche les fichiers dont le contenu contient le terme de recherche
	request.onreadystatechange = function () {
		if (request.readyState == 4 && request.status == 200) {
			communicationIndicatorManager.endRequest();
			var response = JSON.parse(request.responseText);
			if (response.length) {
				for (var i = 0; i < response.length; i++) {
					var line = document.getElementById(response[i].docID);
					line.style.display = "table-row";
					if (searchValue != "") {
						var start = ""
						var end = ""
						if (response[i].containsStart) start = "... ";
						if (response[i].containsEnd) end = " ...";
						// La ligner suivante permet de rajouter le contenu contextualisé
						line.childNodes[1].innerHTML += `<span class = "_search_content additional-data"><br><i class="fa fa-chevron-circle-right" aria-hidden="true"></i>
						&nbsp;${start}${response[i].preContent}<strong>${response[i].content}</strong>${response[i].postContent}${end} </span>`;
					}
				}
			}
		}
	}
}

function select(n) {
	// Cette fonction permet de gérer la selection de lignes sur documents
	// Elle permet d'effectuer les opérations usuelles liées aux touches Shift et Maj
	// On récupère l'élément sur lequel l'utilisateur a cliqué
	var div = document.getElementById(n);
	document.getSelection().removeAllRanges();

	if (!ctrlDown) {
		var divs = document.getElementsByClassName('selected');
		for (i = 0; i < divs.length;) {
			if (divs[i].id != n) divs[i].className = divs[i].className.replace(" selected", '');
			else i++;
		}
	}

	if (shiftDown && lastSelection != -1) {
		var divs = document.getElementsByClassName('_document');
		var inSelection = false;
		var lastDiv = document.getElementById(lastSelection);
		for (i = 0; i < divs.length; i++) {
			if (divs[i].id == n) inSelection = !inSelection;
			if (divs[i].id == lastSelection) inSelection = !inSelection;
			if (inSelection) {
				if (divs[i].className.indexOf("selected") == -1) divs[i].className += " selected";
			}
		}
		if (lastDiv.className.indexOf("selected") == -1) lastDiv.className += " selected";
	}
	else lastSelection = n;

	// Si l'élément n'est pas selectionné, on le selectionne
	if (div.className.indexOf(" selected") != -1) {
		if (!shiftDown) div.className = div.className.replace(" selected", '');
	}
	else div.className += " selected";

	// Si on a des elements selectionnés, on affiche le bouton de suppression
	if (document.getElementsByClassName('selected').length != 0) {
		document.getElementById('_delete').style.display = "inline-block";
		document.getElementById('_delete-value').value = "";
		var divs = document.getElementsByClassName('selected');
		for (i = 0; i < divs.length; i++) {
			document.getElementById('_delete-value').value += divs[i].id;
			if (i != divs.length - 1) document.getElementById('_delete-value').value += ';';
		}
	}
	else document.getElementById('_delete').style.display = "none";

}

var currentTypeOfOrdering = -1;
var ctrlDown = false;
var shiftDown = false;
var lastSelection = -1;

searchDocuments();

// On suit l'activité des touches Shift & Ctrl pour les selections
document.onkeydown = function (event) {
	if (event.ctrlKey) ctrlDown = true;
	if (event.shiftKey) shiftDown = true;
};

document.onkeyup = function (event) {
	if (!event.ctrlKey) ctrlDown = false;
	if (!event.shiftKey) shiftDown = false;
};