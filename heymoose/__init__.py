# -*- coding: utf-8 -*-
from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
import os

app = Flask(__name__)
config_path = os.getenv("FRONTEND_SETTINGS_PATH", "/etc/frontend/config.py")
app.config.from_pyfile(config_path)
mg = MongoAlchemy(app)

import filters
import forms.filters

config=app.config

from heymoose import site, admin, cabinet
app.register_blueprint(site.blueprint, url_prefix='')
app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(cabinet.blueprint, url_prefix='/cabinet')

import handlers
import views.common

#print app.url_map