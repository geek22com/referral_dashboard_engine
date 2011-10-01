# -*- coding: utf-8 -*-
from flask import Flask
import os
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
try:
	config_path = DEBUG_CONFIG
except NameError:
	config_path=os.getenv("FRONTEND_SETTINGS_PATH", "/etc/frontend/config.py")
app.config.from_pyfile(config_path)
mg = MongoAlchemy(app)

config=app.config

def error_type(value, type):
	return filter(lambda x: x[0] == type, value)
app.jinja_env.filters['error_type'] = error_type

#from heymoose.views.admin import admin
from heymoose.views.frontend import frontend
#app.register_module(admin, url_prefix='/admin')
app.register_module(frontend)
print "qqqqqqqqqqqqqq"
