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

@bp.route('/offers/requests')
def offers_requests():
	return render_template('admin/offers/requests.html')

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

@bp.route('/offers/<int:id>/materials')
def offers_info_materials(id):
	offer = rc.offers.get_by_id(id)
	return render_template('admin/offers/info/materials.html', offer=offer)

@bp.route('/offers/<int:id>/requests', methods=['GET', 'POST'])
def offers_info_requests(id):
	offer = rc.offers.get_by_id(id)
	
	filter_args = {
		None: dict(),
		'moderation': dict(state=OfferGrantState.MODERATION, blocked=False),
		'approved': dict(state=OfferGrantState.APPROVED, blocked=False),
		'rejected': dict(state=OfferGrantState.REJECTED, blocked=False),
		'blocked': dict(blocked=True)
	}.get(request.args.get('filter', None), dict())
	
	page = current_page()
	per_page = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
	offset, limit = page_limits(page, per_page)
	grants, count = rc.offer_grants.list(offer_id=offer.id, offset=offset, limit=limit, full=True, **filter_args)
	pages = paginate(page, count, per_page)
	
	form = forms.OfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data)
		if grant and grant.offer.id == offer.id:
			action = form.action.data
			if action == 'unblock':
				rc.offer_grants.unblock(grant.id)
				flash(u'Заявка разблокирована', 'success')
			elif action == 'block':
				rc.offer_grants.block(grant.id, form.reason.data)
				flash(u'Заявка заблокирована', 'success')
			return redirect(request.url)
	return render_template('admin/offers/info/requests.html', offer=offer, grants=grants, pages=pages, form=form)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	offer = rc.offers.get_by_id(id)
	return 'OK'

@bp.route('/offers/<int:id>/actions')
def offers_info_actions(id):
	offer = rc.offers.get_by_id(id)
	return 'OK'