function KeyPress(e){
	control = document.getElementById('SilverlightControl');
	field = document.getElementById('interpreter');
	element = document.getElementById('debugging');
	element2 = document.getElementById('debugging2');
	sel = getSelection(field);
	start = sel.start;
	end = sel.end;
				
	if(window.event) {// IE
		keynum = e.keyCode;
	}
	else if(e.which) { // Netscape/Firefox/Opera
		keynum = e.which;
	}
	else {
		return true;
	}
	
	if ((keynum >= 37) && (keynum < 41)) {
		return true;
	}
	
	keychar = String.fromCharCode(keynum);
	element2.innerHTML = 'KeyNum: ' + keynum + ' KeyChar: ' + keychar;
	retVal = control.Content.onkeypress.method(start, end, keychar);
	element.innerHTML = element.innerHTML + ' Result: ' + retVal;
	if (retVal == 'true') {
		return true;
	} else {
		return false;
	}
}
