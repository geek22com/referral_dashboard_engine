# -*- coding: utf-8 -*-
import json
from restkit.errors import RequestFailed
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.thirdparty.facebook.mongo.data import Performer
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.settings.debug_config import APP_ID, DEVELOPER_SECRET_KEY, APP_SECRET, FACEBOOK_APP_DOMAIN
import heymoose.thirdparty.facebook.actions.oauth as oauth
import heymoose.thirdparty.facebook.actions.base as base
import heymoose.thirdparty.facebook.actions.social_graph as social_graph
import heymoose.thirdparty.facebook.actions.users as users
from heymoose.utils.decorators import oauth_only
import heymoose.forms.forms as forms
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.views.work import flash_form_errors

def get_signed_request():
	signed_request = request.form.get('signed_request', '').decode('utf8')
	if not signed_request:
		signed_request = session.get('signed_request', '')
	return signed_request

def save_signed_request(signed_request):
	session['signed_request'] = signed_request

@frontend.route('/facebook_deauthorize/', methods=['POST'])
def facebook_deauthorize():
	signed_request = get_signed_request()

	valid, data = base.decrypt_request(signed_request)
	if valid:
		app_logger.debug("facebook_deauthorize: user_id={0} remove app".format(data.get(u'user_id')))
	else:
		app_logger.debug("facebook_deauthorize: sign_error")

	return ""

@frontend.route('/facebook_app/', methods=['GET', 'POST'])
def facebook_app():
		signed_request = get_signed_request()
		valid, data = base.decrypt_request(signed_request)
		if valid:
			performer = performers.get_performer(data.get(u'user_id', ''))
			if not performer or performer.dirty:
				performer = Performer(name = data.get(u'name',''),
				                    dirty = False,
								    oauth_token = data.get(u'oauth_token', ''),
								    expires = data.get(u'expires', ''),
								    user_id = data.get(u'user_id', ''),
								    fullname = data.get(u'name'),
								    firstname = data.get(u'first_nam'),
								    lastname = data.get(u'last_name'))
				performer.save()
		else:
			app_logger.debug("facebook_app request Bad Signed")
			abort(404)

		if not oauth.validate_token(performer.oauth_token, 
		                            performer.expires):
			performers.invalidate_performer(performer)
			save_signed_request(signed_request)
			return redirect(url_for('oauth_request'))

		g.params['performer'] = performer
		return render_template('./facebook_app/heymoose-facebook.html', params=g.params)


##################################### AJAX methods #################################################################
@frontend.route('/channel/', methods=['GET', 'POST'])
def channel():
		return render_template('facebook-channel.html', params=g.params)

@frontend.route('/facebook_help', methods=['POST'])
@oauth_only
def facebook_help():
	help_form = forms.FacebookHelpForm(request.form)
	if not help_form.validate():
		app_logger.debug("facebook_help validate error:")
		return json.dumps(help_form.errors)
	
	app_logger.debug("facebook_help email={0}".format(help_form.email.data.decode('utf8')))
	return ""

@frontend.route('/facebook_send_gift', methods=['POST'])
@oauth_only
def facebook_send_gift():
	app_logger.debug("facebook_send_gift {0}".format(request.form))
	gift_form = forms.GiftForm(request.form)
	if not gift_form.validate():
		app_logger.debug("facebook_send_gift form validate error: {0}".format(gift_form.errors))
		abort(406)

	app_logger.debug("facebook_send_gift from_id={0} to_id={1} gift_id={2}".format(gift_form.from_id.data,
																					gift_form.to_id.data,
																					gift_form.gift_id.data))
	return ""

#Let's call it route polymorphism :)
#f.e: you call /facebook_tmpl/gifts
#     if we don't have explicit route for it, then
#     /facebook_tmpl/<tmpl> will be called

@frontend.route('/facebook_tmpl/gifts', methods=['GET', 'POST'])
@oauth_only
def facebook_gifts():
	app_logger.debug("facebook_gifts user_id={0} request={1}".format(g.facebook_user_id,
	                                                                 request.url))
	g.params['friends'] = social_graph.get_friends(g.facebook_user_id, g.access_token)

	return render_template('./facebook_app/gifts.html', params=g.params)

@frontend.route('/facebook_tmpl/<tmpl>', methods=['GET', 'POST'])
def facebook_tmpl(tmpl):
	app_logger.debug("facebook_tmpl/<tmpl>")
	template = "./facebook_app/{0}.html".format(tmpl)
	return render_template(template, params=g.params)
