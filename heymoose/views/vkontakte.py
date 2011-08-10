# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.db.models import Developer
import heymoose.forms.forms as forms
import hashlib

@frontend.route('/vkontakte_app', methods=['GET', 'POST'])
def vkontakte_app():
	happ = {}
	app_developer = Developer.get_vkontakte_app_developer()
	if not app_developer:
		abort(404)

	happ['app_id'] = app_developer.app_id

	secret = app_developer.secret_key
	req_sig = hashlib.md5()
	req_sig.update(str(happ['app_id']) + secret)

	happ['sig'] = req_sig.hexdigest()
	happ['user_id'] = request.args.get('user_id', '0')
	g.params['happ'] = happ
	return render_template('heymoose-vkontakte.html', params=g.params)
