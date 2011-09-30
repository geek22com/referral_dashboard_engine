# -*- coding: utf-8 -*-
import json
from restkit.errors import RequestFailed
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.thirdparty.facebook.mongo.data import Performer, Offers, OffersStat, Gifts
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose import config
import heymoose.thirdparty.facebook.actions.oauth as oauth
import heymoose.thirdparty.facebook.actions.base as base
import heymoose.thirdparty.facebook.actions.social_graph as social_graph
import heymoose.thirdparty.facebook.actions.users as users
from heymoose.utils.decorators import oauth_only
import heymoose.forms.forms as forms
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.thirdparty.facebook.mongo.data import Donations
from heymoose.views.work import flash_form_errors

@frontend.route('/facebook_deauthorize/', methods=['GET','POST'])
@oauth_only
def facebook_deauthorize():
	signed_request = request.form.get('signed_request', '').decode('utf8')

	valid, data = base.decrypt_request(signed_request)
	if valid:
		app_logger.debug("facebook_deauthorize: user_id={0} remove app".format(data.get(u'user_id')))
	else:
		app_logger.debug("facebook_deauthorize: sign_error")

	return ""

#This is entry point to facebook_app, Every user start from here, and in case of
#not g.performer or g.performer.dirty you must redirect user here
@frontend.route('/facebook_app/', methods=['GET', 'POST'])
def facebook_app():
		if not g.performer:
			signed_request = request.form.get('signed_request', '').decode('utf8')
			valid, data = base.decrypt_request(signed_request)
			if valid and data:
				performer = Performer(dirty = False,
								    oauth_token = data.get(u'oauth_token', ''),
								    expires = data.get(u'expires', ''),
								    user_id = data.get(u'user_id', ''),
							        fullname = data.get(u'name'),
								    firstname = data.get(u'first_name'),
								    lastname = data.get(u'last_name'))
				performer.save()
				g.performer = performer
				session['performer_id'] = g.performer.user_id
			else:
				app_logger.debug("facebook_app request Bad Signed")
				abort(404)

		if not oauth.validate_token(g.performer.oauth_token,
									g.performer.expires):
			performers.invalidate_performer(g.performer)
			g.performer.save()
			return redirect(url_for('oauth_request'))

		if g.performer.dirty:
			fresh_performer_obj = users.get_user(g.performer.user_id,
													g.performer.oauth_token)
			performers.reload_performer_info(g.performer, fresh_performer_obj)
			g.performer.save()

		g.params['app_id'] = config.get('APP_ID')
		g.params['app_domain'] = config.get('FACEBOOK_APP_DOMAIN')
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

@frontend.route('/facebook_do_offer', methods=['POST'])
@oauth_only
def facebook_do_offer():
	offer_form = forms.OfferForm(request.form)
	if not offer_form.validate():
		app_logger.debug("facebook_do_offer offerform validate error: {0}".format(offer_form.errors))
		abort(406)
	offer_stat = OffersStat(performer_id = g.performer.user_id,
							offer_id = offer_form.offer_id.data)
	offer_stat.save()
	return ""

@frontend.route('/facebook_send_gift', methods=['POST'])
@oauth_only
def facebook_send_gift():
	app_logger.debug("facebook_send_gift {0}".format(request.form))
	gift_form = forms.GiftForm(request.form)
	if not gift_form.validate():
		app_logger.debug("facebook_send_gift form validate error: {0}".format(gift_form.errors))
		abort(406)

	if str(g.performer.user_id) != gift_form.from_id.data:
		app_logger.debug("Break attempt from performer_id={0}".format(g.performer.user_id))

	gift = Gifts.query.filter(Gifts.mongo_id == gift_form.gift_id.data).first()
	if not gift:
		abort(407) #Show something in the interface

	if gift.price > g.performer.amount:
		abort(408) #Show something in the interface

	g.performer.amount = g.performer.amount - gift.price
	g.performer.donations += dict(to_id=gift_form.to_id.data,
									gift_id=gift.mongo_id)
	g.performer.save()
	
	app_logger.debug("facebook_send_gift from_id={0} to_id={1} gift_id={2}".format(g.performer.user_id,
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
	app_logger.debug("facebook_gifts user_id={0} request={1}".format(g.performer.user_id,
	                                                                 request.url))
	try:
		g.params['friends'] = social_graph.get_friends(g.performer.user_id,
		                                               g.performer.oauth_token)
	except Exception:
		#Facebook OAuth Error request
		performers.invalidate_performer(g.performer)
		g.performer.save()

	g.params['gifts'] = Gifts.query.filter(Gifts.price <= g.performer.amount).all()
	return render_template('./facebook_app/gifts.html', params=g.params)

@frontend.route('/facebook_tmpl/stat', methods=['GET', 'POST'])
@oauth_only
def facebook_stat():
	app_logger.debug("facebook_stat performer_id={0} request={1}".format(g.performer.user_id,
		                                                                    request.url))
	#g.params['offers'] = OffersStat.query.filter().all()
	return render_template('./facebook_app/stat.html', params=g.params)

@frontend.route('/facebook_tmpl/<tmpl>', methods=['GET', 'POST'])
def facebook_tmpl(tmpl):
	app_logger.debug("facebook_tmpl/<tmpl>")
	template = "./facebook_app/{0}.html".format(tmpl)
	return render_template(template, params=g.params)
