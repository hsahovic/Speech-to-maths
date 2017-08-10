function fill_viewport () {
	var el = document.getElementById('white_body_filler');
	var total_height = window.innerHeight;
	var el_pos = el.getBoundingClientRect();
	console.log(total_height - el_pos.top);
	el.style.height = (total_height - el_pos.top).toString() + 'px';
}

fill_viewport ()
window.addEventListener("resize", fill_viewport, false);