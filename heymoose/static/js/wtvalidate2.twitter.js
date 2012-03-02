function showError2(field, message) {
	field.closest('.clearfix').addClass('error');
	field.closest('.input').find('.errors').empty();
	if (message)
		field.closest('.input').find('.errors')
			.append($('<span>').addClass('help-block').text(message));
}

function clearError2(field) {
	field.closest('.clearfix').removeClass('error');
	field.closest('.input').find('.errors').empty();
}

var twitterValidateHandlers2 = { error: showError2, clear: clearError2 };
