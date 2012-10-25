# -*- coding: utf-8 -*-
import os
from flask import Flask
from assets import configure_assets

app = Flask(__name__)

def configure(app):
	config_path = os.getenv('FRONTEND_SETTINGS_PATH', '/etc/frontend/config.py')
	print ' * Using config file {0}'.format(config_path)
	app.config.from_pyfile(config_path)
	app.logger
	from logging.config import dictConfig
	dictConfig(app.config.get('LOGGING'))

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