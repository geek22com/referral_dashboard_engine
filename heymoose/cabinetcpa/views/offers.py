# -*- coding: utf-8 -*-
from flask import request, flash, g, redirect, url_for, abort, jsonify, send_file
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import Offer, OfferGrant, SubOffer, Banner
from heymoose.data.enums import OfferGrantState
from heymoose.notifications import notify
from heymoose.views import excel
from heymoose.views.decorators import template, paginated, sorted
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only, affiliate_only
import base64

OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
OFFER_REQUESTS_PER_PAGE = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
OFFER_ACTIONS_PER_PAGE = app.config.get('OFFER_ACTIONS_PER_PAGE', 20)

def existing_offer(id):
	return rc.offers.get_by_id(id)

def requested_offer(id):
	return rc.offers.get_requested(id, g.user.id)

def visible_offer(id):
	'''
	For both advertisers and affiliates. For advertiser returns offer only if it is his offer
	or if this offer is visible (approved, active, launched). For affiliate returns offer only
	if offer is granted for this affiliate or if it is visible. Otherwise returns 404.
	'''
	if g.user.is_advertiser:
		offer = rc.offers.get_by_id(id)
		if offer.owned_by(g.user) or offer.visible:
			return offer
	else:
		offer = rc.offers.get_try_requested(id, g.user.id)
		if offer.grant or offer.visible:
			return offer
	abort(404)

def my_offer(id):
	'''
	For advertisers only. Returns offer if it is owned by current advetiser.
	Otherwise returns 404.
	'''
	offer = existing_offer(id)
	if not offer.owned_by(g.user): abort(404)
	return offer

def approved_requested_offer(id):
	'''
	For affiliates only. Returns offer if it has approved grant for current affiliate.
	Otherwise returns 404.
	'''
	offer = requested_offer(id)
	if not offer.grant or not offer.grant.approved: abort(404)
	return offer

@bp.route('/offers/')
@template('cabinetcpa/offers/all.html')
@paginated(OFFERS_PER_PAGE)
def offers_all(**kwargs):
	form = forms.OfferFilterForm(request.args)
	kwargs.update(form.backend_args())
	if g.user.is_affiliate: kwargs.update(aff_id=g.user.id)
	offers, count = rc.offers.list(approved=True, active=True, launched=True, **kwargs) if form.validate() else ([], 0)
	return dict(offers=offers, count=count, form=form)

@bp.route('/offers/my')
@advertiser_only
@template('cabinetcpa/offers/list.html')
@paginated(OFFERS_PER_PAGE)
def offers_list(**kwargs):
	offers, count = rc.offers.list(advertiser_id=g.user.id, **kwargs)
	return dict(offers=offers, count=count)

@bp.route('/offers/requested')
@affiliate_only
@template('cabinetcpa/offers/requested.html')
@paginated(OFFERS_PER_PAGE)
def offers_requested(**kwargs):
	offers, count = rc.offers.list_requested(g.user.id, **kwargs)
	return dict(offers=offers, count=count)


@bp.route('/offers/products/')
@affiliate_only
@template('cabinetcpa/offers/products.html')
def offers_products():
	catalog = rc.products.feed(g.user.id)
	shops = rc.products.categories(g.user.id)
	return dict(products=catalog.products, shops=shops)


@bp.route('/offers/new', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/new.html')
def offers_new():
	tmpl = forms.SubOfferForm(prefix='suboffers-0-')
	form = forms.OfferForm(request.form)
	if request.method == 'POST' and form.validate():
		offer = Offer(advertiser=g.user)
		form.populate_obj(offer)
		suboffers = []
		for suboffer_field in form.suboffers:
			suboffer = SubOffer()
			suboffer_field.form.populate_obj(suboffer)
			suboffers.append(suboffer)
		id = rc.offers.add(offer, 0.00)
		for suboffer in suboffers:
			rc.offers.add_suboffer(id, suboffer)
		flash(u'Оффер успешно создан', 'success')
		return redirect(url_for('.offers_info', id=id))
	return dict(form=form, tmpl=tmpl)

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/info.html')
def offers_info(id):
	offer = visible_offer(id)
	offer.overall_debt = rc.withdrawals.overall_debt(offer_id=offer.id)
	if g.user.is_affiliate and not offer.grant and request.method == 'POST' and 'request' in request.form:
		offer_grant = OfferGrant(offer=offer, affiliate=g.user)
		rc.offer_grants.add(offer_grant)
		flash(u'Заявка на сотрудничество успешно отправлена', 'success')
		return redirect(request.url)
	return dict(offer=offer)

@bp.route('/offers/<int:id>/edit', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/edit.html')
def offers_info_edit(id):
	offer = my_offer(id)
	form = forms.OfferEditForm(request.form, obj=offer)
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
@template('cabinetcpa/offers/info/actions.html')
def offers_info_actions(id):
	offer = visible_offer(id)
	if offer.exclusive: abort(403)
	form = forms.SubOfferForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/actions/edit', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/actions-edit.html')
def offers_info_actions_main_edit(id):
	offer = my_offer(id)
	if offer.exclusive: abort(403)
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
	return dict(offer=offer, suboffer=offer, form=form)

@bp.route('/offers/<int:id>/actions/<int:sid>/edit', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/actions-edit.html')
def offers_info_actions_edit(id, sid):
	offer = my_offer(id)
	if offer.exclusive: abort(403)
	suboffer = offer.suboffer_by_id(sid)
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

@bp.route('/offers/<int:id>/materials', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/materials.html')
def offers_info_materials(id):
	offer = visible_offer(id)
	form = forms.OfferBannerForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		banner = Banner()
		form.populate_obj(banner)
		image_base64 = base64.encodestring(request.files['image'].stream.read())
		rc.offers.add_banner(offer.id, banner, image_base64)
		flash(u'Баннер успешно загружен', 'success')
		return redirect(request.url)
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/materials/<int:bid>/delete')
@advertiser_only
def offers_info_materials_delete(id, bid):
	offer = my_offer(id)
	if not offer.banner_by_id(bid): abort(404)
	rc.offers.delete_banner(id, bid)
	flash(u'Баннер удален', 'success')
	return redirect(url_for('.offers_info_materials', id=id))

@bp.route('/offers/<int:id>/materials/up/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/materials-upload.html')
def offers_info_materials_upload(id):
	offer = my_offer(id)
	if request.method == 'POST':
		form = forms.OfferBannerForm(request.form)
		if form.validate():
			banner = Banner()
			form.populate_obj(banner)
			f = request.files['image']
			image_base64 = base64.encodestring(f.stream.read())
			rc.offers.add_banner(offer.id, banner, image_base64)
			return jsonify(name=f.name)
		else:
			return jsonify(error=form.image.errors[0])
	return dict(offer=offer)

@bp.route('/offers/<int:id>/requests', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/requests.html')
@sorted('affiliate_id', 'asc')
@paginated(OFFER_REQUESTS_PER_PAGE)
def offers_info_requests(id, **kwargs):
	offer = my_offer(id)
	filter_args = {
		None: dict(),
		'moderation': dict(state=OfferGrantState.MODERATION, blocked=False),
		'approved': dict(state=OfferGrantState.APPROVED, blocked=False),
		'rejected': dict(state=OfferGrantState.REJECTED, blocked=False),
		'blocked': dict(blocked=True)
	}.get(request.args.get('filter', None), dict())
	kwargs.update(filter_args)
	grants, count = rc.offer_grants.list(offer_id=offer.id, full=False, **kwargs)
	
	form = forms.OfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		if grant and grant.offer.id == offer.id and not grant.blocked:
			action = form.action.data
			if action == 'approve' and not grant.approved:
				rc.offer_grants.approve(grant.id)
				notify.grant_approved(grant)
				flash(u'Заявка утверждена', 'success')
			elif action == 'reject' and not grant.rejected:
				rc.offer_grants.reject(grant.id, form.reason.data)
				notify.grant_rejected(grant, form.reason.data)
				flash(u'Заявка отклонена', 'success')
			return redirect(request.url)
	return dict(offer=offer, grants=grants, count=count, form=form)

@bp.route('/offers/<int:id>/sales/', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/sales.html')
@sorted('creation_time', 'desc')
@paginated(OFFER_ACTIONS_PER_PAGE)
def offers_info_sales(id, **kwargs):
	offer = my_offer(id)
	if request.method == 'POST':
		if 'approve' in request.form:
			rc.actions.approve_by_ids(offer.id, request.form.getlist('id'))
			flash(u'Действия подтверждены', 'success')
		elif 'cancel' in request.form:
			rc.actions.cancel_by_ids(offer.id, request.form.getlist('id'))
			flash(u'Действия отменены', 'success')
		return redirect(request.url)
	form = forms.OfferActionsFilterForm(request.args)
	kwargs.update(form.backend_args())
	if request.args.get('format', '') == 'xls':
		actions, _ = rc.actions.list(offer.id, offset=0, limit=999999, **form.backend_args()) if form.validate() else ([], 0)
		if actions:
			return send_file(excel.offer_actions_to_xls(actions), as_attachment=True, attachment_filename='actions.xls')
		else:
			flash(u'Не найдено ни одного действия', 'danger')
			return redirect(request.url)
	else:
		actions, count = rc.actions.list(offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, actions=actions, count=count, form=form)

@bp.route('/offers/<int:id>/settings', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/offers/info/settings.html')
def offers_info_settings(id):
	offer = approved_requested_offer(id)
	grant = offer.grant
	form = forms.OfferGrantForm(request.form, obj=grant)
	if request.method == 'POST' and form.validate():
		form.populate_obj(grant)
		if grant.updated():
			rc.offer_grants.update(grant)
			flash(u'Настройки успешно обновлены', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(request.url)
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/stats')
@template('cabinetcpa/offers/info/stats.html')
def offers_info_stats(id):
	offer = visible_offer(id)
	return dict(offer=offer)

