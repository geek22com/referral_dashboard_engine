(function($) {
	function categoryChecked(category) {
		return category.find('li input[type=checkbox]:checked').length ==
			category.find('li input[type=checkbox]').length;
	}
	
	$.fn.categorizedList = function() {
		return this.each(function() {
			var categNames = [];
			var categListItems = [];
			
			$(this).find('input').each(function() {
				var categName = $(this).data('category');
				if (!categName) return;
				
				var index = $.inArray(categName, categNames);
				var $categListItem = null;
				if (index < 0) {
					categNames.push(categName);
					$categListItem = $('<li>')
						.attr('class', 'category')
						.append($('<input>')
							.attr('type', 'checkbox')
							.attr('class', 'category-checkbox')
							.change(function() {
								$(this).closest('li').find('input[type=checkbox]')
									.attr('checked', $(this).is(':checked'));
							}))
						.append($('<label>')
							.append($('<a>')
								.attr('href', '#')
								.attr('class', 'category-collapse')
								.text(categName)
								.click(function() {
									$(this).closest('li').find('ul').toggle();
									return false;
								})))
						.append($('<ul>').attr('class', 'category-list'));
					categListItems.push($categListItem);
				}
				else
					$categListItem = categListItems[index];
				
				$(this).change(function() {
					var liCategory = $(this).closest('li.category');
					liCategory.find('input.category-checkbox').attr('checked', categoryChecked(liCategory));
				}).closest('li').appendTo($categListItem.find('ul'));
			});
			
			$.each(categListItems, function() {
				$(this).appendTo($('ul.categorized'));
				if (categoryChecked($(this))) {
					$(this).find('input.category-checkbox').attr('checked', true)
					$(this).find('ul').toggle();
				}
			});
		});
	}
})(jQuery);
