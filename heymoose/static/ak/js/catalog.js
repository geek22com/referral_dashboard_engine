$(function() {
	var regions = [];
	var regionsNameToCodeMap = {};
	var regionsCodeToNameMap = {};
	
	function AddRegion(name) {
		if (name in regionsNameToCodeMap
			&& !$('.b-filter-region .b-categories-list__item a:contains("' + name + '")').length) {
			$('.b-filter-region').find('.b-categories-list').append('<li class="b-categories-list__item"><a class="b-link-icon" href="#"><i class="b-ico b-ico_delete"></i>' + name + '</a></li>');
			return true;
		}
		return false;
	}
	
	function UpdateCatalog(page) {
		$('.b-btn-sudmit').hide();
		$('.b-wait-indicator').show();
		
		var regionCodes = [];
		$('.b-filter-region .b-categories-list a').each(function() {
			var region = $(this).text(); 
			if (region in regionsNameToCodeMap) {
				regionCodes.push(regionsNameToCodeMap[region])
			}
		});
		
		var segments = [];
		$('.b-filter-segment .b-categories-list li.b-active-element').each(function() {
			segments.push($(this).data('id'));
		});
		
		var paymentTypes = [];
		$('.b-filter-pay .b-categories-list li.b-active-element').each(function() {
			paymentTypes.push($(this).data('id'));
		});
		
		var exclusive = $('.b-filter-exclusive.b-active-element').length > 0;
		
		$.ajax('/catalog/page/', {
			type: 'get',
			dataType: 'json',
			traditional: true,
			data: {
				region: regionCodes,
				category: segments,
				payment_type: paymentTypes,
				exclusive: (exclusive ? 'y' : undefined),
				offset: (page ? $('.b-offers-list > li').length : 0)
			}
		}).success(function(data) {
			if (!page) {
				$('.b-offers-list').empty();
			}
			if (data.offers.length) {
				$('#offer-template').tmpl(data.offers).appendTo('.b-offers-list');				
			} else {
				$('#notify-container').notify('create', {
					title: 'Список пуст',
					text: 'Больше нет офферов, удовлетворяющих запросу'
				});
			}
		}).error(function(jqXHR, textStatus) {
			$('#notify-container').notify('create', {
				title: 'Не удается загрузить список',
				text: 'Ошибка ' + jqXHR.status
			});
		}).complete(function() {
			$('.b-wait-indicator').hide();
			var hasOffers = $('.b-offers-list > li').length > 0
			$('.b-btn-sudmit').toggle(hasOffers);
			$('.b-no-more-offers').toggle(!hasOffers);
		});
	}
	
	$('.b-filter-list__item').click(function () {
		if (!$(this).hasClass('b-filter-list__item_active')) {
			var filterList = $(this).parent();
			filterList.find('.b-filter-list__item').removeClass('b-filter-list__item_active');
			$(this).addClass('b-filter-list__item_active');
			CheckFilterItemActive();
		}
	});
	
	// REGIONS FILTER STUFF
	
	$('#regions-list li').each(function() {
		var regionCode = $(this).data('code');
		var regionName = $(this).text();
		regions.push(regionName);
		regionsNameToCodeMap[regionName] = regionCode;
		regionsCodeToNameMap[regionCode] = regionName;
	});
	
	$("#regions").autocomplete({ source: regions });
	
	$('.b-show-field').click(function () {
		$('.b-region-field').show();
		$(this).hide();
	});
	
	var csi = ['RU', 'UA', 'BY', 'KZ', 'AM', 'AZ', 'KG', 'MD', 'TJ', 'TM', 'UZ'];
	$('.b-add-csi').click(function() {
		$.each(csi, function(i, code) { AddRegion(regionsCodeToNameMap[code]); });
		UpdateCatalog();
	});
	
	$('.b-clear-regions').click(function() {
		$('.b-filter-region .b-categories-list').empty();
		UpdateCatalog();
	});

	$('.b-region-cancel').click(function () {
		$('.b-region-field').hide();
		$('.b-show-field').show();
	});

	$('.b-filter-region .b-categories-list__item a').live('click', function () {
		$(this).parent().remove();
		UpdateCatalog();
		return false;
	});

	$('#regions').keyup(function (e) {
		var input = $(e.target);
		var value = $.trim(input.val());
		if (e.which == 13 && value.length && AddRegion(value)) {
			input.val('');
			$('.b-region-field').hide();
			$('.b-show-field').show();
			UpdateCatalog();
		}
	});

	// SEGMENTS FILTER STUFF

	$('.b-filter-segment a').click(function () {
		$(this).parent().toggleClass('b-active-element');
		UpdateCatalog();
	});
	
	// PAY FILTER STUFF

	$('.b-filter-pay a').click(function () {
		var li = $(this).parent();
		if (li.hasClass('b-active-element')) {
			li.removeClass('b-active-element');
		} else {
			$(this).closest('.b-categories-list').find('.b-categories-list__item').removeClass('b-active-element');
			li.addClass('b-active-element');
		}
		UpdateCatalog();
	});
	
	$('.b-filter-exclusive').click(function () {
		$(this).toggleClass('b-active-element');
		UpdateCatalog();
	});
	
	// OTHER STUFF

	$('.b-clear-filter').click(function () {
		$('.b-active-element').removeClass('b-active-element');
		$('.b-filter-region .b-categories-list').empty();
		AddRegion('Россия');
		UpdateCatalog();
	});

	$('.b-btn-sudmit').click(function() {
		UpdateCatalog(true);
	});
	
	UpdateCatalog();
});

$(document).click(function (e) {
	var target = $(e.target);
	if (!(target.parents('.b-filter').length + target.parents('.ui-autocomplete').length)) {
		$('.b-filter-list__item_active').removeClass('b-filter-list__item_active');
		CheckFilterItemActive();
	}
});

function CheckFilterItemActive() {
	$('.b-filter-list__item').each(function () {
		var filter = $(this);
		if (filter.find('.b-active-element').length) {
			$(filter).addClass('b-active-element');
		} else {
			$(filter).removeClass('b-active-element');
		}
	});
}
