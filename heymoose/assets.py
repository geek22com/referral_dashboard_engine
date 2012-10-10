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
		filters=['rjsmin'], output='ak/js/site.js'
	))
	assets.register('site_css', Bundle(
		'ak/css/default.css',
		'ak/css/icons.css',
		'ak/css/components.css',
		'ak/css/forms.css',
		'ak/css/jquery.fancybox.css',
		'ak/css/ui.notify.css',
		'ak/css/override.css',
		output='ak/css/site.css'
	))