// Javascript version of 'to_icon' macro
function toIcon(elem, value) {
	if (value)
		elem.html('<img src="/static/img/icon-yes.gif" alt="да" />');
	else
		elem.html('<img src="/static/img/icon-no.gif" alt="нет" />');
}
