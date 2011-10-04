# -*- coding: utf-8 -*-
import json
from restkit.errors import RequestFailed
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.thirdparty.facebook.actions import base
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose import config
import heymoose.forms.forms as forms

def offer_callback(data):
#	offer_stat = OffersStat.query.filter(OffersStat.performer_id == "1", OffersStat.offer_id == "12").first()
#	if offer_stat:
#		offer_stat.done = True
#		offer_stat.save()
#	else:
#		offer_stat = OffersStat(performer_id="12",
#								offer_id = "23",
#								done = True)
#		offer_stat.save()
#		app_logger.debug("offer_callback on unexistend offerstat performer_id={0} offer_id={1}".format(1,2))
#
#	performer = performers.get_performer("12")
#	if not performer:
#		app_logger.debug("offer_callback on unexistend performer performer_id={0}".format(1,2))
#
#	performer.amount = performer.amount + 123
#	performer.save()
	pass

def mlm_callback(data):
	pass

@frontend.route('/main_callback/', methods=['POST'])
def main_callback():
	signed_request = request.form.get('signed_request', '').decode('utf8')

	valid, data = base.decrypt_request(signed_request)
	if valid:
		type = data.get('type')
		if type == 'offer':
			offer_callback(data)
		elif type == 'mlm':
			mlm_callback(data)
		else:
			app_logger.debug('main_callback: unknown callback type = {0}'.format(type))
	else:
		app_logger.debug("bad signed request: sign_error")

	return ""

