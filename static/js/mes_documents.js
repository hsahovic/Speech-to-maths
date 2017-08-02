function cacher () {
	var div = document.getElementsByClassName("confirm")[0];
	div.style.display = "none";
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
		if (classement == 2) {
			vara = a.getElementsByTagName('input')[0].value.split(' ');
			varb = b.getElementsByTagName('input')[0].value.split(' ');
			for (i = 0 ; i < vara.length ; i++) {
				if (parseInt(vara[i]) > parseInt(varb[i])) {
					return 1;
				}
			}
			return -1;
		}
		if (a.getElementsByTagName("td")[classement].textContent > b.getElementsByTagName("td")[classement].textContent) {
			return 1;
		}
		return -1;
	});
	icons = document.getElementsByClassName("_decoration");
	for (var i = 0; i < icons.length ; i++) {
		icons[i].remove();
	}
	if (classement_courant == classement) {
		lignes.reverse();
		classement_courant = -1;
		table_head[classement].innerHTML += "<i class='fa fa-arrow-up _decoration' aria-hidden='true'></i>";
	}
	else {
		classement_courant = classement;
		table_head[classement].innerHTML += "<i class='fa fa-arrow-down _decoration' aria-hidden='true'></i>";
	}
	for (var i = 0; i < lignes.length ; i++) {
		table.appendChild(lignes[i]);
	}
	return 0;
}

function select (n) {
	var div = document.getElementById(n);
	if (div.className.indexOf(" selected") == -1) {
		var divs = document.getElementsByClassName('selected');
		for (i=0 ; i < divs.length ; i++) {
			divs[i].className = divs[i].className.replace(" selected", '');
		}
		div.className += " selected";
	}
	else {
		div.className = div.className.replace(" selected", '');
	}
	if (document.getElementsByClassName('selected').length != 0) {
		document.getElementById('_delete').style.visibility = "visible";
		document.getElementById('_delete-value').value = n;
	}
	else {
		document.getElementById('_delete').style.visibility = "hidden";
	}
}

classement_courant = -1;
search();