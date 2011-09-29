# -*- coding: utf-8 -*-
import hashlib
import random
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.thirdparty.facebook.actions.oauth as oauth
from heymoose import config
FACEBOOK_APP_URL = config.get('FACEBOOK_APP_URL')

#TODO: is it simplier to store TokenObject in session?
#Server-side flow implementation: http://developers.facebook.com/docs/authentication/
@frontend.route("/facebook_app/oauth_request", methods=["GET"])
def oauth_request():
	if not session.has_key('state'):
		session['state'] = hashlib.md5(str(random.randint(0, 4000000000))).hexdigest()
		return redirect(oauth.get_oauth_dialog_url(redirect_url=url_for('oauth_request',
		                                                                _external=True),
												csrf_protect=session['state'],
												scope='publish_stream'))

	if session['state'] != request.args.get('state', ''):
		app_logger.debug("CSRF attempt")
		abort(404) #CSRF attempt

	if request.args.get('error', '') == 'access_denied':
		app_logger.debug("Access denied")
		abort(405) #So, then you can't use our app, TODO:generate something special here

	token, expires = oauth.get_acces_token(redirect_url=url_for('oauth_request',
													_external=True),
                                                code=request.args.get('code'))
	if not token:
		app_logger.debug("Access_token error")
		abort(406) #Facebook send us OAuthRequest error

	session['access_token'] = token
	session['expires'] = oauth.expires_to_absolute_epoch(expires)

	return redirect(FACEBOOK_APP_URL)
