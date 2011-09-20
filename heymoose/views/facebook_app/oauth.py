# -*- coding: utf-8 -*-
import hashlib
import random
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.views.frontend import frontend
import heymoose.thirdparty.facebook.actions.oauth as oauth

#Server-side flow implementation: http://developers.facebook.com/docs/authentication/
@frontend.route("/oauth_request", methods=["GET"])
def oauth_request():
	if not getattr(session, 'state'):
		session['state'] = hashlib.md5(str(random.randint(0, 4000000000))).hexdigest()
		return redirect(oauth.get_oauth_dialog_url(redirect_url='/oauth_request',
												csrf_protect=session['state']))

	if session['state'] != request.args.get('state', ''):
		abort(404) #CSRF attempt

	if request.args.get('error', '') == 'access_denied':
		abort(404) #So, then you can't use our app, TODO:generate something special here

	session['access_token'] = oauth.get_acces_token(redirect_url=url_for('facebook_app'),
	                                                code=request.args.get('code'))
	return redirect(url_for('facebook_app'))
