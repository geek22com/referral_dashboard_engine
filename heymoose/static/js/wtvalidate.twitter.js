function showError(field, type) {
	field.parent().parent().addClass('error');
	field.parent().find('span.help-block').remove();
	
	var msg = $('#' + field.attr('id') + '-msg-' + type).html();
	if (msg) field.parent().append('<span class="help-block">' + msg + '</span>');
}

function clearError(field) {
	field.parent().parent().removeClass('error');
	field.parent().find('span.help-block').remove();
}

var twitterValidateHandlers = { error: showError, clear: clearError };
