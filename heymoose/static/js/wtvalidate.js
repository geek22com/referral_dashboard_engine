(function($) {
	$.fn.validateRequired = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val().trim() == '') {
				error(field, 'required');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateRange = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var min = parseFloat(field.closest('.formfield').find('#' + field.attr('id') + '-min').html());
			var max = parseFloat(field.closest('.formfield').find('#' + field.attr('id') + '-max').html());
			var val = parseFloat(field.val())
			
			var ok = !isNaN(val) && ((isNaN(min) && isNaN(max)) ||
					 (!isNaN(min) && !isNaN(max) && val >= min && val <= max) ||
					 (isNaN(min) && val <= max) || (isNaN(max) && val >= min));
			
			if (!ok) {
				error(field, 'range');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateLength = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var min = parseInt($('#' + field.attr('id') + '-min').html());
			var max = parseInt($('#' + field.attr('id') + '-max').html());
			var val = field.val().length;
			
			if (isNaN(min)) min = -1;
			if (isNaN(max)) max = -1;
			
			var ok = !isNaN(val) && ((min < 0 && max < 0) ||
					 (min >= 0 && max >= 0 && val >= min && val <= max) ||
					 (min < 0 && val <= max) || (max < 0 && val >= min));
			
			if (!ok) {
				error(field, 'length');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateUrl = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (field.val() == '') return;
			
			var regexp = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
			if (!regexp.test(field.val())) {
				error(field, 'url');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateEqual = function(error) {
		var valid = true;
		this.each(function() {
			var field1 = $(this);
			var other_id = $('#' + field1.attr('id') + '-other').html();
			var field2 = $('#' + other_id);
			if (field1.val() != field2.val()) {
				error(field1, 'equal');
				error(field2, 'equal');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateDecimal = function(error) {
		var valid = true;
		this.each(function() {
			var field = $(this);
			if (isNaN(parseFloat(field.val().trim()))) {
				error(field, 'decimal');
				valid = false;
			}
		});
		return valid;
	}
	
	$.fn.validateForm = function(options) {
		var defaults = {
			error: function(field, type) { },
			clear: function(field) { }
		}
		var settings = $.extend(defaults, options);
		
		return this.each(function() {
			$(this).find('input,textarea').keypress(function() {
				settings.clear($(this));
			});
			
			$(this).find('input[type=file]').click(function() {
				settings.clear($(this));
			});
			
			return $(this).submit(function() {
				var valid = true;
				valid = $(this).find('.validate-required').validateRequired(settings.error) && valid;
				valid = $(this).find('.validate-range').validateRange(settings.error) && valid;
				valid = $(this).find('.validate-length').validateLength(settings.error) && valid;
				valid = $(this).find('.validate-url').validateUrl(settings.error) && valid;
				valid = $(this).find('.validate-equal').validateEqual(settings.error) && valid;
				valid = $(this).find('.validate-decimal').validateDecimal(settings.error) && valid;
				return valid;
			});
		});
	}
})(jQuery);

