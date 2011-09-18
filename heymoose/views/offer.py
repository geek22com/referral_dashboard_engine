# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
import hashlib

def create_sig(developer):
	req_sig = hashlib.md5()
	req_sig.update(str(developer.app_id) + developer.secret_key)
	return req_sig.hexdigest()

@frontend.route('/test_offer', methods=['GET', 'POST'])
def test_offer():
	return render_template('get_offers_test.html')

@frontend.route('/add_offer', methods=['GET', 'POST'])
@admin_only
def add_offer():
	if request.method == 'POST':
		offer = Offer(title=request.form['offertitle'],
						body=request.form['offerbody'],
						url=request.form['offerurl'],
						time=request.form['offertime'],
						voice=request.form['offervoice'])
		if not offer:
			abort(404)

		offer.save()
		return redirect(url_for('add_offer'))

	return render_template('add-offer.html', params=g.params)

@frontend.route('/get_offers', methods=['GET', 'POST'])
def get_offers():
	pass
#	offer_form = forms.OfferForm(request.form)
#	if request.method == 'POST' and offer_form.validate():
#		developer = Developer.get_by_app_id(offer_form.app_id.data)
#		if not developer:
#			app_logger.debug('No such developer ' + str(offer_form.app_id.data))
#			abort(404)
#
#		if not developer.check_sign(offer_form.sig.data):
#			app_logger.debug('Bad check_sign ' + str(offer_form.sig.data))
#			abort(403)
#
#		offers = OfferFormer.get_offer_form()
#		if not offers:
#			app_logger.debug('No offer')
#			abort(405)
#
#		g.params['offers'] = offers
#		g.params['developer'] = developer
#		g.params['sig'] = create_sig(developer)
#		g.params['error_url'] = 'http://www.404.ru/'
#		return render_template('offer-template.html', params=g.params)
#	else:
#		app_logger.debug('Bad request or form validate')
#		app_logger.debug(offer_form.errors)
#		abort(400)

@frontend.route('/do_offer', methods=['GET', 'POST'])
def do_offer():
	pass
#	offer_form = forms.OfferForm(request.form)
#	if request.method == 'POST' and offer_form.validate():
#		user_id_int = offer_form.user_id.data / 4000000000  # Fix bug with Bigint in database
#		developer = Developer.get_by_app_id(offer_form.app_id.data)
#		if not developer:
#			app_logger.debug('No such developer ' + str(offer_form.app_id.data))
#			abort(404)
#
#		if not developer.check_sign(offer_form.sig.data):
#			app_logger.debug('Bad check_sign ' + str(offer_form.sig.data))
#			abort(403)
#
#		if not Offer.isOfferAvailable(user_id_int, offer_form.offer_id.data):
#			return render_template('offer-error.html')
#
#		offer = Offer.get_offer_by_id(offer_form.offer_id.data)
#		if not offer:
#			return redirect(location=offer_form.error_url)
#
#		offer.save_stat(user_id_int, developer.app_id, offer.voice, 0)
#		return redirect(location=offer.url)
#	else:
#		app_logger.debug('Bad request or form validate')
#		app_logger.debug(offer_form.errors)
#		app_logger.debug(request.method)
#		abort(400)
