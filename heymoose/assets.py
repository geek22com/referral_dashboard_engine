# -*- coding: utf-8 -*-

def configure_assets(app):
	from flask.ext.assets import Environment, Bundle
	assets = Environment(app)
	assets.register('site_js', Bundle(
		'ak/js/jquery.min.js',
		'ak/js/jquery-ui-1.8.22.custom.min.js',
		'ak/js/jquery.notify.js',
		'ak/js/slides.min.jquery.js',
		'ak/js/jquery.fancybox.pack.js',
		'ak/js/jquery.jcarousel.min.js',
		'ak/js/jquery.tmpl.min.js',
		'js/wtvalidate2.js',
		'ak/js/common.js',
		filters=['rjsmin'], output='ak/js/site.gen.js'
	))
	assets.register('site_catalog_js', Bundle(
		'ak/js/catalog.js',
		filters=['rjsmin'], output='ak/js/site.catalog.gen.js'
	))
	assets.register('site_css', Bundle(
		'ak/css/default.css',
		'ak/css/icons.css',
		'ak/css/components.css',
		'ak/css/forms.css',
		'ak/css/jquery.fancybox.css',
		'ak/css/ui.notify.css',
		'ak/css/override.css',
		output='ak/css/site.gen.css'
	))
	assets.register('site_ie_css', Bundle(
		'ak/css/ie.css',
		output='ak/css/site.ie.gen.css'
	))
	assets.register('cabinet_js', Bundle(
		'js/jquery-latest.js',
		'js/jquery-ui.min.js',
		'js/jquery.ui.datepicker-ru.js',
		'js/jquery-ui-timepicker-addon.js',
		'js/jquery.form.js',
		'js/bootstrap-dropdown.js',
		'js/bootstrap-modal.js',
		'js/bootstrap-alerts.js',
		'js/wtvalidate2.js',
		'js/wtvalidate2.twitter.js',
		'js/categorized.list.js',
		'js/data-list.js',
		filters=['rjsmin'], output='js/cabinet.gen.js'
	))
	assets.register('cabinet_css', Bundle(
		'css/timepicker-addon.css',
		'css/bootstrap.min.css',
		'css/bootstrap.hm.css',
		'css/roundbox.css',
		'css/lists.css',
		'css/forms.css',
		'css/pills-filter.css',
		'css/newsitem.css',
		'css/redactor-text.css',
		'css/disqus.css',
		output='css/cabinet.gen.css'
	))