function KeyPress(e){
	control = document.getElementById('SilverlightControl');
	field = document.getElementById('interpreter');
	// element = document.getElementById('debugging');
	// element2 = document.getElementById('debugging2');
	sel = getSelection(field);
	start = sel.start;
	end = sel.end;
				
	if(window.event) {// IE
		keynum = e.keyCode;
		ctrl = e.ctrlKey;
	}
	else if(e.which) { // Netscape/Firefox/Opera
		keynum = e.which;
		ctrl = e.ctrlKey || e.metaKey;
	}
	else {
	    // unknown browser
		return true;
	}
	
	// document.getElementById('debugging').innerHTML = keynum
	// document.getElementById('debugging2').innerHTML = ctrl
	// document.getElementById('debugging3').innerHTML = String.fromCharCode(keynum);
	
	if ((keynum >= 33) && (keynum < 41)) {
		return true;
	}
	
	var mask = /[aczyACZY]/;

	keychar = String.fromCharCode(keynum);
	if (mask.test(keychar) && ctrl) {
	    return true;
	} 
	// element2.innerHTML = 'KeyNum: ' + keynum + ' KeyChar: ' + keychar;
	retVal = control.Content.onkeypress.method(start, end, keychar);
	// element.innerHTML = element.innerHTML + ' Result: ' + retVal;
	if (retVal == 'true') {
		return true;
	} else {
		return false;
	}
}
