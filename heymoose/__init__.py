# -*- coding: utf-8 -*-
from flask import Flask, g, session, request
from flaskext.mongoalchemy import MongoAlchemy
import os

app = Flask(__name__)
config_path = os.getenv("FRONTEND_SETTINGS_PATH", "/etc/frontend/config.py")
app.config.from_pyfile(config_path)
mg = MongoAlchemy(app)

import filters
import forms.filters

config=app.config

from heymoose import site, admin, cabinetcpa
app.register_blueprint(site.blueprint, url_prefix='')
app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(cabinetcpa.blueprint, url_prefix='/cabinet')

from heymoose.resource import users

@app.before_request
def before_request():
	g.user = None
	g.config = app.config
	g.params = {}
	
	if 'user_id' in session and '/static' not in request.url and '/upload' not in request.url:
		print '\n'
		g.user = users.get_by_id(int(session['user_id']))

from views import common, testapi

#print app.url_map