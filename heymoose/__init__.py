# -*- coding: utf-8 -*-
from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.from_pyfile("./settings/debug_config.py")
mg = MongoAlchemy(app)

def error_type(value, type):
	return filter(lambda x: x[0] == type, value)
app.jinja_env.filters['error_type'] = error_type

#from heymoose.views.admin import admin
from heymoose.views.frontend import frontend
#app.register_module(admin, url_prefix='/admin')
app.register_module(frontend)
