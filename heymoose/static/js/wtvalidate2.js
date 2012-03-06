(function($) {
	$.fn.validateRequired2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);			
			if (field.is('ul') && !field.find(':checked').length ||
				!field.is('ul') && field.val().trim() == '') {
				error(field, field.data('requiredMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateRange2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var min = parseFloat(field.data('rangeMin'));
			var max = parseFloat(field.data('rangeMax'));
			var val = parseFloat(field.val())
			
			var ok = !isNaN(val) && ((isNaN(min) && isNaN(max)) ||
					 (!isNaN(min) && !isNaN(max) && val >= min && val <= max) ||
					 (isNaN(min) && val <= max) || (isNaN(max) && val >= min));
			
			if (!ok) {
				error(field, field.data('rangeMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateLength2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var min = parseInt(field.data('lengthMin'));
			var max = parseInt(field.data('lengthMax'));
			var val = field.val().length;
			
			if (isNaN(min)) min = -1;
			if (isNaN(max)) max = -1;
			
			var ok = !isNaN(val) && ((min < 0 && max < 0) ||
					 (min >= 0 && max >= 0 && val >= min && val <= max) ||
					 (min < 0 && val <= max) || (max < 0 && val >= min));
			
			if (!ok) {
				error(field, field.data('lengthMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateUrl2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var regexp = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
			if (!regexp.test(field.val())) {
				error(field, field.data('urlMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateEqual2 = function(error) {
		var valid = true;
		this.each(function() {
			var field1 = $(this);
			var field2 = $('#' + field1.data('equalOther'));
			if (field1.val() != field2.val()) {
				error(field1, field1.data('equalMessage'));
				error(field2, field2.data('equalMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateDecimal2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (isNaN(parseFloat(field.val().trim()))) {
				error(field, field.data('decimalMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateInteger2 = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (isNaN(parseInt(field.val().trim()))) {
				error(field, field.data('integerMessage'));
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateForm2 = function(options) {
		var defaults = {
			error: function(field, type) { },
			clear: function(field) { }
		}
		var settings = $.extend(defaults, options);
		
		return this.each(function() {
			$(this).find('input,textarea').keypress(function() {
				settings.clear($(this));
			});
			
			$(this).find('input,textarea').change(function() {
				settings.clear($(this));
			});
			
			$(this).find('input[type=file]').click(function() {
				settings.clear($(this));
			});
			
			return $(this).submit(function() {
				var valid = true;
				valid = $(this).find('.validate-required').validateRequired2(settings.error) && valid;
				valid = $(this).find('.validate-range').validateRange2(settings.error) && valid;
				valid = $(this).find('.validate-length').validateLength2(settings.error) && valid;
				valid = $(this).find('.validate-url').validateUrl2(settings.error) && valid;
				valid = $(this).find('.validate-equal').validateEqual2(settings.error) && valid;
				valid = $(this).find('.validate-decimal').validateDecimal2(settings.error) && valid;
				valid = $(this).find('.validate-integer').validateInteger2(settings.error) && valid;
				return valid;
			});
		});
	}
})(jQuery);

