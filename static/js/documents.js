function orderLines(typeOfOrdering) {
	// Cette fonction permet de classer les lignes de la table contenant les informations de nos documents, selon un critère : 0 correspond au titre, 1 à l'auteur, 2 à la date
	var lines = [].slice.call(document.getElementsByClassName("_document"));
	var table = document.getElementsByTagName("table")[0];
	var table_head = table.getElementsByTagName("th");
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
		table_head[typeOfOrdering].innerHTML += "<i class='fa fa-arrow-up _decoration' aria-hidden='true'></i>";
	}
	else {
		currentTypeOfOrdering = typeOfOrdering;
		table_head[typeOfOrdering].innerHTML += "<i class='fa fa-arrow-down _decoration' aria-hidden='true'></i>";
	}
	for (var i = 0; i < lines.length; i++) {
		table.appendChild(lines[i]);
	}
	console.log(table.innerHTML);
	return 0;
}

function searchDocuments() {
	// Cette fonction permet de gérer les recherches sur la page documents
	// On récupère le terme recherché
	var search_value = document.getElementsByTagName("input")[0].value.toLowerCase();

	var lines = document.getElementsByClassName("_document");

	// On envoie une requête au serveur interrogeant le contenu des documents
	var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
	var formData = new FormData;
	var request = new XMLHttpRequest();
	request.open("POST", documents_search_link);
	request.setRequestHeader("X-CSRFToken", csrftoken)
	formData.append("searchValue", search_value);
	request.send(formData);

	// On effectue une recherche sur les contenus des lignes
	for (var i = 0; i < lines.length; i++) {
		if (lines[i].textContent.toLowerCase().indexOf(search_value) >= 0) {
			lines[i].style.display = "table-row";
		}
		else {
			lines[i].style.display = "none";
		}
	}

	// Une fois la recherche effectuée, et une fois notre requête receptionnée en bonne et due forme, on affiche les fichiers dont le contenu contient le terme de recherche
	request.onreadystatechange = function () {
		if (request.readyState == 4 && request.status == 200) {
			var search_result = request.responseText;
			var resultIndices = search_result.split(';');
			if (resultIndices[0] != "") {
				for (var i = 0; i < resultIndices.length; i++) {
					document.getElementById(resultIndices[i]).style.display = "table-row";
				}
			}
		}
	}
}

function select(n) {
	// On récupère l'élément sur lequel l'utilisateur a cliqué
	var div = document.getElementById(n);
	var div_is_selected = (div.className.indexOf(" selected") != -1)
	document.getSelection().removeAllRanges();

	if (!ctrl_down) {
		var divs = document.getElementsByClassName('selected');
		// Je ne comprends pas pourquoi la ligne suivante fonctionne.
		for (i = 0; i < divs.length;) divs[0].className = divs[0].className.replace(" selected", '');
	}

	// Si l'élément n'est pas selectionné, on le selectionne
	if (div_is_selected) div.className = div.className.replace(" selected", '');
	else div.className += " selected";

	// Si on a des elements selectionnés, on affiche le bouton de suppression
	if (document.getElementsByClassName('selected').length != 0) {
		document.getElementById('_delete').style.visibility = "visible";
		document.getElementById('_delete-value').value = "";
		var divs = document.getElementsByClassName('selected');
		for (i = 0; i < divs.length; i++) {
			document.getElementById('_delete-value').value += divs[i].id;
			if (i != divs.length - 1) document.getElementById('_delete-value').value += ';';
		}
	}
	else document.getElementById('_delete').style.visibility = "hidden";
}

currentTypeOfOrdering = -1;
ctrl_down = false;
shift_down = false;

searchDocuments();

// On suit l'activité des touches Shift & Ctrl pour les selections
document.onkeydown = function (event) {
	if (event.ctrlKey) ctrl_down = true;
	if (event.shiftKey) shift_down = true;
};

document.onkeyup = function (event) {
	if (!event.ctrlKey) ctrl_down = false;
	if (!event.shiftKey) shift_down = false;
};