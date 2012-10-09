# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

def configure(app):
	config_path = os.getenv('FRONTEND_SETTINGS_PATH', '/etc/frontend/config.py')
	print ' * Using config file {0}'.format(config_path)
	app.config.from_pyfile(config_path)

def configure_assets(app):
	from flask.ext.assets import Environment
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

def app_init_basic(app):
	configure(app)

def app_init_assets(app):
	configure(app)
	configure_assets(app)

def app_init_web(app):
	configure(app)
	configure_assets(app)
	# Import handlers and filters
	import handlers, filters, forms.filters
	# Import and register views and blueprints
	from views import common
	from heymoose import site, admin, cabinetcpa
	app.register_blueprint(site.blueprint, url_prefix='')
	app.register_blueprint(admin.blueprint, url_prefix='/admin')
	app.register_blueprint(cabinetcpa.blueprint, url_prefix='/cabinet')
	# print app.url_map