(function($) {
	$.fn.dataList = function(options) {
		var defaults = {};
		var settings = $.extend(defaults, options);

		return this.each(function() {
			var selectAllCheckbox = $(this).find('.data-list-select-all-checkbox:first');
			var itemCheckboxes = $(this).find('.data-list-item-checkbox');
			var actionTriggers = $('.' + $(this).data('actionClass'));

			selectAllCheckbox.change(function() {
				itemCheckboxes.attr('checked', $(this).is(':checked'));
				actionTriggers.attr('disabled', !itemCheckboxes.filter(':checked').length);
			}).change();

			itemCheckboxes.change(function() {
				var allChecked = (itemCheckboxes.length == itemCheckboxes.filter(':checked').length);
				selectAllCheckbox.attr('checked', allChecked);
				actionTriggers.attr('disabled', !itemCheckboxes.filter(':checked').length);
			}).change();
		});
	}
})(jQuery);