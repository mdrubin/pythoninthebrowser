
var is_gecko = /gecko/i.test(navigator.userAgent);
var is_ie    = /MSIE/.test(navigator.userAgent);


function getSelection(field) {
    if (is_gecko)
    	return { start: field.selectionStart, end: field.selectionEnd };
    
		var r = document.selection.createRange();
		if (r == null) {
			return { start: 0, end: field.value.length }
		}
		
		var re = field.createTextRange();
		var rc = re.duplicate();
		re.moveToBookmark(r.getBookmark());
		rc.setEndPoint('EndToStart', re);
		
		return { start: rc.text.length, end: rc.text.length + r.text.length };
		
};
