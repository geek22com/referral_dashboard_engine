$(document).ready(function () {
	var notifier = $('#notify-container').notify();
	$('#notify-messages li').each(function() {
		var category = $(this).data('category');
		notifier.notify('create', {
			title: (category == 'danger' || category == 'error' ? 'Ошибка' : 'Информация'),
			text: $(this).html()
		});
	});
	
	$('.validate2').validateForm2({
		error: showFieldError,
		clear: clearFieldError
	});

	$('.b-carousel_screens').jcarousel({
		scroll: 1,
		visible: 1
	});

	$('.b-carousel_landings').jcarousel({
		scroll: 1,
		visible: 4
	});

	// Set starting slide to 1
	var startSlide = 1;
	// Get slide number if it exists
	if (window.location.hash) {
		startSlide = window.location.hash.replace('#', '');
	}

	$("#slides").slides({
		generateNextPrev: true,
		generatePagination: true,
		effect: 'fade',
		// Get the starting slide
		start: startSlide,
		next: 'b-next',
		prev: 'b-prev',
		animationComplete: function (current) {
			// Set the slide number as a hash
			window.location.hash = '#' + current;
			CheckSlideStep('slides');
		}
	});
	$(".b-contest-accordion").accordion({
		event: "mouseover"
	});



	$('.b-screens-list__item a').fancybox({
		padding: 0,
		margin: 70,
		helpers: {
			title: null
		}
	});

	if (!$('.b-footer .b-bottom__in .b-logo-artkadabra').length) {
		$('.b-footer .b-bottom__in').prepend('<a style="background: url(http://dl.dropbox.com/u/46315398/logo-artkadabra.png) no-repeat top left;display: block; height: 52px; left: 32px; position: absolute; text-decoration: none; text-indent: -9999px; top: -4px; width: 32px;" href="http://artkadabra.ru/" class="b-logo-artkadabra">Artkadabra</a>');
	}

	$('.b-show-popup').fancybox({
		padding: 0,
		margin: 0,
		helpers: { title: null },
		afterShow: function () {
			this.content.find('input:first').focus();
		}
	});

	CheckSlideStep('slides');

	$('.b-slider').mouseenter(function () {
		if ($('.slider-overlay').length == 0) {
			$(this).parents('.b-slider-wrap').addClass('hovered');
			$('body').append('<div class="slider-overlay"></div>');
			$('.slider-overlay').css('opacity', 0).animate({
				opacity: 0.8
			}, 500)
		}
	});

	$('.b-slider').mouseleave(function () {
		if ($('.slider-overlay').length == 1) {
			$(this).parents('.b-slider-wrap').removeClass('hovered');
			$('.slider-overlay').stop().animate({
				opacity: 0
			}, 500, function () {
				$('.slider-overlay').remove()
			});

		}
	});

	var availableTags = ["Армения", "Азербайджан", "Киргизия", "Таджикистан", "Молдавия", "Туркмения", "Узбекистан", "Беларусь", "Эстония", "Латвия", ];
	$("#regions").autocomplete({
		source: availableTags
	});


	$('.b-filter-list__item').click(function () {
		if (!$(this).hasClass('b-filter-list__item_active')) {
			var filterList = $(this).parent();
			filterList.find('.b-filter-list__item').removeClass('b-filter-list__item_active');
			$(this).addClass('b-filter-list__item_active');
			CheckFilterItemActive();
		}
	});

	$('.b-categories-list__item a').click(function () {
		$(this).parent().toggleClass('b-active-element');
		var block = $(this).parents('.b-categories-list');
		var title = block.prev('.b-category_title');

		if (block.find('.b-categories-list__item').length == block.find('.b-categories-list__item.b-active-element').length) {
			title.addClass('b-active-element');
		} else {
			title.removeClass('b-active-element');
		}
	});

	$('.b-filter-exclusive').click(function () {
		$(this).toggleClass('b-active-element');
	});

	$('.b-category_title').click(function () {
		$(this).toggleClass('b-active-element');

		if ($(this).hasClass('b-active-element')) {
			$(this).next('.b-categories-list').find('.b-categories-list__item').addClass('b-active-element');
		} else {
			$(this).next('.b-categories-list').find('.b-categories-list__item').removeClass('b-active-element');
		}
	});

	$('.b-clear-filter').click(function () {
		$('.b-active-element').removeClass('b-active-element');
	});

	$('.b-show-field').click(function () {
		$('.b-region-field').show();
		$(this).hide();
	});

	$('.b-region-cancel').click(function () {
		$('.b-region-field').hide();
		$('.b-show-field').show();
	});

	$('.b-filter-region .b-categories-list__item a').live('click', function () {
		$(this).parent().remove();
		return false;
	});

	$('#regions').keyup(function (e) {
		var input = $(e.target);
		if (e.which == 13 && input.val().length) {
			$(this).parents('.b-filter-region').find('.b-categories-list').append('<li class="b-categories-list__item"><a class="b-link-icon" href="#"><i class="b-ico b-ico_delete"></i>' + input.val() + '</a></li>');
			input.val('');
			$('.b-region-field').hide();
			$('.b-show-field').show();
		}
	});
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

	$('.b-view-more-offers .b-link-toggle').click(function () {
		$('.b-view-more-offers').hide();
		$('.b-pagination').show();
	});

	$('.b-pagination .b-link-toggle').click(function () {
		$('.b-pagination').hide();
		$('.b-view-more-offers').show();
	});
}


function CheckSlideStep(slidesAreaId) {
	var slidesArea = $('#' + slidesAreaId);
	var items = slidesArea.find('.b-slides-list__item');
	var prevBtn = slidesArea.find('.b-prev');
	var nextBtn = slidesArea.find('.b-next');

	if (items.length > 0) {
		if (items.first().css('display') != 'none') {
			prevBtn.hide();
			nextBtn.show();
		} else if (items.last().css('display') != 'none') {
			prevBtn.hide();
			nextBtn.hide();
		} else {
			prevBtn.show();
			nextBtn.show();
		}
	}
}

function clearFieldError(field) {
	field.removeClass('b-field-error');
	field.closest('.b-field').find('.b-field-error-text').remove();
}

function showFieldError(field, message) {
	field.addClass('b-field-error');
	var fieldWrap = field.closest('.b-field');
	fieldWrap.find('.b-field-error-text').remove();
	if (message) {
		$('<div>').addClass('b-field-error-text').text(message).appendTo(fieldWrap);
	}
}
