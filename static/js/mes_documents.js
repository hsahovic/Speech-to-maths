function cacher () {
	var div = document.getElementsByClassName("confirm")[0];
	div.style.display = "none";
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
				if (parseInt(vara[i]) < parseInt(varb[i])) {
					return -1;
				}
			}
			return -1;
		}
		if (a.getElementsByTagName("td")[classement].textContent.toLowerCase() > b.getElementsByTagName("td")[classement].textContent.toLowerCase()) {
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

function search () {
	var lignes = document.getElementsByClassName("_document");
	var search_value = document.getElementsByTagName("input")[0].value.toLowerCase();	
	for (var i = 0; i < lignes.length ; i++) {
		if(lignes[i].textContent.toLowerCase().indexOf(search_value) >= 0) {
			lignes[i].style.display = "table-row";
		}
		else {
			lignes[i].style.display = "none";
		}
	}
}

function select (n) {
	// On récupère l'élément sur lequel l'utilisateur a cliqué
	var div = document.getElementById(n);
	var div_is_selected = (div.className.indexOf(" selected") != -1)
	document.getSelection().removeAllRanges();
	
	if (!ctrl_down) {
		var divs = document.getElementsByClassName('selected');
		// Je ne comprends pas pourquoi la ligne suivante fonctionne.
		for (i=0 ; i < divs.length ;) divs[0].className = divs[0].className.replace(" selected", '');
	}
	
	// Si l'élément n'est pas selectionné, on le selectionne
	if (div_is_selected) div.className = div.className.replace(" selected", '');
	else div.className += " selected";
	
	// Si on a des elements selectionnés, on affiche le bouton de suppression
	if (document.getElementsByClassName('selected').length != 0) {
		document.getElementById('_delete').style.visibility = "visible";
		document.getElementById('_delete-value').value = "";
		var divs = document.getElementsByClassName('selected');
		for (i=0 ; i < divs.length; i++) {
			document.getElementById('_delete-value').value += divs[i].id;
			if (i != divs.length -1) document.getElementById('_delete-value').value += ';';
		}
	}
	else document.getElementById('_delete').style.visibility = "hidden";
}

classement_courant = -1;
ctrl_down = false;
shift_down = false;

search();

// On suit l'activité des touches Shift & Ctrl pour les selections
document.onkeydown = function (event) {
	if (event.ctrlKey) ctrl_down = true;
	if (event.shiftKey) shift_down = true;
};

document.onkeyup = function (event) {
	if (!event.ctrlKey) ctrl_down = false;
	if (!event.shiftKey) shift_down = false;
};