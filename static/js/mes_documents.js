function cacher () {
	var div = document.getElementsByClassName("confirm")[0];
	div.style.display = "none";
}

function confirmation (lien, nom) {
	var div = document.getElementsByClassName("confirm")[0];
	div.style.display = "block";
	div.getElementsByClassName("_contenu")[0].innerHTML = nom;
	div.getElementsByTagName("a")[0].href = lien;
	div.getElementsByTagName("li")[1].addEventListener("click", cacher); 
}

function search () {
	var lignes = document.getElementsByClassName("_document");
	var search_value = document.getElementsByTagName("input")[0].value.toLowerCase();	
	for (var i = 0; i < lignes.length ; i++) {
		if(lignes[i].textContent.toLowerCase().indexOf(search_value) >= 0) {
			lignes[i].className = "_document";
		}
		else {
			lignes[i].className = "_document cache";
		}
	}
}

function classer(classement) {
	var lignes = [].slice.call(document.getElementsByClassName("_document"));
	var table = document.getElementsByTagName("table")[0];
	var table_head = table.getElementsByTagName("th");
	var icons = 0;
	
	lignes.sort(function(a,b) {
		if (a.getElementsByTagName("td")[classement].textContent > b.getElementsByTagName("td")[classement].textContent) {
			return 1;
		}
		return -1;
	});
	for (var i = 0; i < table_head.length ; i++) {
		icons = table_head[i].getElementsByTagName("i");
		for (var j = 0; j < icons.length ; j++) {
			icons[j].remove();
		}
	}
	if (classement_courant == classement) {
		lignes.reverse();
		classement_courant = -1;
		table_head[classement].innerHTML += "<i class='fa fa-arrow-up' aria-hidden='true'></i>";
	}
	else {
		classement_courant = classement;
		table_head[classement].innerHTML += "<i class='fa fa-arrow-down' aria-hidden='true'></i>";
	}
	for (var i = 0; i < lignes.length ; i++) {
		table.appendChild(lignes[i]);
	}
	return 0;
}

classement_courant = -1;
search();