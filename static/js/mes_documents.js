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

search();