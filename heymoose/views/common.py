# -*- coding: utf-8 -*-
from flask import send_from_directory, abort
from heymoose import app


@app.route('/upload/<path:filename>')
def upload(filename):
	if app.config.get('DEBUG', False):
		return send_from_directory(app.config.get('UPLOAD_PATH', ''), filename)
	else:
		abort(403)


@app.route('/products/feed/')
def xml_feed():
	abort(403)