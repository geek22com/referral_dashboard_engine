# -*- coding: utf-8 -*-
from flask import render_template, request, flash, g, redirect, url_for, abort
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import Offer, OfferGrant, SubOffer
from heymoose.data.enums import OfferGrantState
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.admin import blueprint as bp


@bp.route('/offers/')
def offers_list():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list(offset=offset, limit=limit)
	pages = paginate(page, count, per_page)
	return render_template('admin/offers/list.html', offers=offers, pages=pages)

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
def offers_info(id):
	offer = rc.offers.get_by_id(id)
	form = forms.OfferBlockForm(request.form)
	if request.method == 'POST' and form.validate():
		action = request.form.get('action')
		if action == 'block':
			rc.offers.block(offer.id, form.reason.data)
			flash(u'Оффер заблокирован', 'success')
		elif action == 'unblock':
			rc.offers.unblock(offer.id)
			flash(u'Оффер разблокирован', 'success')
		return redirect(request.url)
	return render_template('admin/offers/info/info.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	offer = rc.offers.get_by_id(id)
	return 'OK'

@bp.route('/offers/<int:id>/actions')
def offers_info_actions(id):
	offer = rc.offers.get_by_id(id)
	return 'OK'