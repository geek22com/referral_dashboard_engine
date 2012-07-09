# -*- coding: utf-8 -*-
from flask import request, flash, redirect, url_for, abort
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import SubOffer
from heymoose.data.enums import OfferGrantState
from heymoose.mail import transactional as mail
from heymoose.views.decorators import template, sorted, paginated
from heymoose.admin import blueprint as bp

OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
OFFER_REQUESTS_PER_PAGE = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
AFFILIATE_STATS_PER_PAGE = app.config.get('AFFILIATE_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)


@bp.route('/offers/')
@template('admin/offers/list.html')
@paginated(OFFERS_PER_PAGE)
def offers_list(**kwargs):
	offers, count = rc.offers.list(**kwargs)
	return dict(offers=offers, count=count)

@bp.route('/offers/requests', methods=['GET', 'POST'])
@template('admin/offers/requests.html')
@paginated(OFFER_REQUESTS_PER_PAGE)
def offers_requests(**kwargs):	
	filter_args = {
		None: dict(),
		'new': dict(blocked=True, moderation=True),
		'blocked': dict(blocked=True, moderation=False),
		'unblocked': dict(blocked=False),
		'moderation': dict(state=OfferGrantState.MODERATION, blocked=False),
		'approved': dict(state=OfferGrantState.APPROVED, blocked=False),
		'rejected': dict(state=OfferGrantState.REJECTED, blocked=False),
	}.get(request.args.get('filter', None), dict())
	kwargs.update(filter_args)
	grants, count = rc.offer_grants.list(full=True, **kwargs)
	
	form = forms.AdminOfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		action = form.action.data
		if action == 'unblock':
			rc.offer_grants.unblock(grant.id)
			grant.blocked = False
			if form.mail.data and grant.approved:
				mail.user_grant_approved(grant.offer, grant.affiliate)
			flash(u'Заявка разблокирована', 'success')
		elif action == 'block':
			rc.offer_grants.block(grant.id, form.reason.data)
			if form.mail.data:
				mail.user_grant_blocked(grant.offer, grant.affiliate, form.reason.data)
			flash(u'Заявка заблокирована', 'success')
		elif action == 'approve' and not grant.approved:
			rc.offer_grants.approve(grant.id)
			if form.mail.data and not grant.blocked:
				mail.user_grant_approved(grant.offer, grant.affiliate)
			flash(u'Заявка утверждена', 'success')
		elif action == 'reject' and not grant.rejected:
			rc.offer_grants.reject(grant.id, form.reason.data)
			if form.mail.data:
				mail.user_grant_rejected(grant.offer, grant.affiliate, form.reason.data)
			flash(u'Заявка отклонена', 'success')
		return redirect(request.url)
	return dict(grants=grants, count=count, form=form)

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
@template('admin/offers/info/info.html')
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
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/edit', methods=['GET', 'POST'])
@template('admin/offers/info/edit.html')
def offers_info_edit(id):
	offer = rc.offers.get_by_id(id)
	form = forms.AdminOfferEditForm(request.form, obj=offer)
	if request.method == 'POST' and form.validate():
		form.populate_obj(offer)
		if offer.updated():
			rc.offers.update(offer)
			flash(u'Оффер успешно изменен', 'success')
			return redirect(url_for('.offers_info', id=offer.id))
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/actions/', methods=['GET', 'POST'])
@template('admin/offers/info/actions.html')
def offers_info_actions(id):
	offer = rc.offers.get_by_id(id)	
	form = forms.SubOfferForm(request.form)
	if request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/actions/edit', methods=['GET', 'POST'])
@template('admin/offers/info/actions-edit.html')
def offers_info_actions_main_edit(id):
	offer = rc.offers.get_by_id(id)
	suboffer = offer
	form = forms.MainSubOfferForm(request.form, obj=offer)
	form.offer_id = offer.id
	if request.method == 'POST' and form.validate():
		form.populate_obj(offer)
		if offer.updated():
			rc.offers.update(offer)
			flash(u'Действие успешно изменено', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.offers_info_actions', id=offer.id))
	return dict(offer=offer, suboffer=suboffer, form=form)

@bp.route('/offers/<int:id>/actions/<int:sid>/edit', methods=['GET', 'POST'])
@template('admin/offers/info/actions-edit.html')
def offers_info_actions_edit(id, sid):
	offer = rc.offers.get_by_id(id)
	suboffer = None
	for sub in offer.all_suboffers:
		if sub.id == sid: suboffer = sub
	if not suboffer: abort(404)
	form = forms.SubOfferForm(request.form, obj=suboffer)
	form.offer_id = suboffer.id
	if request.method == 'POST' and form.validate():
		form.populate_obj(suboffer)
		if suboffer.updated():
			rc.offers.update_suboffer(offer.id, suboffer)
			flash(u'Действие успешно изменено', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.offers_info_actions', id=offer.id))
	return dict(offer=offer, suboffer=suboffer, form=form)


@bp.route('/offers/<int:id>/materials')
@template('admin/offers/info/materials.html')
def offers_info_materials(id):
	offer = rc.offers.get_by_id(id)
	return dict(offer=offer)

@bp.route('/offers/<int:id>/requests', methods=['GET', 'POST'])
@template('admin/offers/info/requests.html')
@paginated(OFFER_REQUESTS_PER_PAGE)
def offers_info_requests(id, **kwargs):
	offer = rc.offers.get_by_id(id)
		
	filter_args = {
		None: dict(),
		'new': dict(blocked=True, moderation=True),
		'blocked': dict(blocked=True, moderation=False),
		'unblocked': dict(blocked=False),
		'moderation': dict(state=OfferGrantState.MODERATION, blocked=False),
		'approved': dict(state=OfferGrantState.APPROVED, blocked=False),
		'rejected': dict(state=OfferGrantState.REJECTED, blocked=False),
	}.get(request.args.get('filter', None), dict())
	kwargs.update(filter_args)
	grants, count = rc.offer_grants.list(offer_id=offer.id, full=True, **kwargs)
	
	form = forms.AdminOfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		if grant and grant.offer.id == offer.id:
			action = form.action.data
			if action == 'unblock':
				rc.offer_grants.unblock(grant.id)
				grant.blocked = False
				if form.mail.data and grant.approved:
					mail.user_grant_approved(grant.offer, grant.affiliate)
				flash(u'Заявка разблокирована', 'success')
			elif action == 'block':
				rc.offer_grants.block(grant.id, form.reason.data)
				if form.mail.data:
					mail.user_grant_blocked(grant.offer, grant.affiliate, form.reason.data)
				flash(u'Заявка заблокирована', 'success')
			elif action == 'approve' and not grant.approved:
				rc.offer_grants.approve(grant.id)
				if form.mail.data and not grant.blocked:
					mail.user_grant_approved(grant.offer, grant.affiliate)
				flash(u'Заявка утверждена', 'success')
			elif action == 'reject' and not grant.rejected:
				rc.offer_grants.reject(grant.id, form.reason.data)
				if form.mail.data:
					mail.user_grant_rejected(grant.offer, grant.affiliate, form.reason.data)
				flash(u'Заявка отклонена', 'success')
			return redirect(request.url)
	return dict(offer=offer, grants=grants, count=count, form=form)

@bp.route('/offers/<int:id>/operations', methods=['GET', 'POST'])
@template('admin/offers/info/operations.html')
def offers_info_operations(id):
	offer = rc.offers.get_by_id(id)
	if request.method == 'POST':
		type = request.form.get('type', '')
		if type == 'approve':
			count = rc.actions.approve_expired(offer_id=offer.id)
			flash(u'{0} действий подтверждено'.format(count), 'success')
		elif type == 'cancel' and 'csv' in request.files:
			transactions = [t.strip() for t in request.files['csv'].read().split(',')]
			count = rc.actions.cancel_by_transactions(offer.id, transactions)
			flash(u'{0} действий отменено'.format(count), 'success')
		return redirect(request.url)
	return dict(offer=offer)

@bp.route('/offers/<int:id>/stats/affiliate')
@template('admin/offers/info/stats/affiliate.html')
@sorted('clicks_count', 'desc')
@paginated(AFFILIATE_STATS_PER_PAGE)
def offers_info_stats_affiliate(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_affiliate_by_offer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/referer')
@template('admin/offers/info/stats/referer.html')
@sorted('clicks_count', 'desc')
@paginated(REFERER_STATS_PER_PAGE)
def offers_info_stats_referer(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_referer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/keywords')
@template('admin/offers/info/stats/keywords.html')
@sorted('clicks_count', 'desc')
@paginated(KEYWORDS_STATS_PER_PAGE)
def offers_info_stats_keywords(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count, form=form)
