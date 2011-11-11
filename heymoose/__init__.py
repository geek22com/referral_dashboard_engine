# -*- coding: utf-8 -*-
from flask import Flask
import os
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
config_path = os.getenv("FRONTEND_SETTINGS_PATH", "/etc/frontend/config.py")
app.config.from_pyfile(config_path)
mg = MongoAlchemy(app)

import filters

config=app.config

from heymoose.views.frontend import frontend
from heymoose import admin


app.register_module(frontend)
app.register_blueprint(admin.blueprint, url_prefix='/admin')

#print app.url_map