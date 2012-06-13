# -*- coding: utf-8 -*-
from flask import render_template, request, flash, g, redirect, url_for, abort, jsonify
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import Offer, OfferGrant, SubOffer, Banner
from heymoose.data.enums import OfferGrantState
from heymoose.mail import transactional as mail
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.utils.convert import to_unixtime
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only, affiliate_only
import base64


@bp.route('/offers/')
def offers_all():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	aff_id_arg = dict(aff_id=g.user.id) if g.user.is_affiliate else dict()
	offers, count = rc.offers.list(offset=offset, limit=limit, approved=True, active=True, launched=True, **aff_id_arg)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/all.html', offers=offers, pages=pages)

@bp.route('/offers/my')
@advertiser_only
def offers_list():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list(offset=offset, limit=limit, advertiser_id=g.user.id)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/list.html', offers=offers, pages=pages)

@bp.route('/offers/requested')
@affiliate_only
def offers_requested():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list_requested(g.user.id, offset=offset, limit=limit)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/offers/requested.html', offers=offers, pages=pages)

@bp.route('/offers/new', methods=['GET', 'POST'])
@advertiser_only
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
	return render_template('cabinetcpa/offers/new.html', form=form, tmpl=tmpl)

@bp.route('/offers/stats')
def offers_stats():
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 10)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_user(g.user, offset=offset, limit=limit,
			**{'from' : to_unixtime(form.dt_from.data, True), 'to' : to_unixtime(form.dt_to.data, True)})
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/offers/stats.html', stats=stats, pages=pages, form=form)

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
def offers_info(id):
	offer = rc.offers.get_try_requested(id, g.user.id) if g.user.is_affiliate else rc.offers.get_by_id(id)
	form = forms.OfferRequestForm(request.form)
	if g.user.is_affiliate and not offer.grant and request.method == 'POST' and form.validate():
		offer_grant = OfferGrant(offer=offer, affiliate=g.user, message=form.message.data)
		rc.offer_grants.add(offer_grant)
		flash(u'Заявка на сотрудничество успешно отправлена', 'success')
		return redirect(url_for('.offers_requested'))
	return render_template('cabinetcpa/offers/info/info.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/edit', methods=['GET', 'POST'])
@advertiser_only
def offers_info_edit(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	form = forms.OfferEditForm(request.form, obj=offer)
	if request.method == 'POST' and form.validate():
		form.populate_obj(offer)
		if offer.updated():
			rc.offers.update(offer)
			flash(u'Оффер успешно изменен', 'success')
			return redirect(url_for('.offers_info', id=offer.id))
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
	return render_template('cabinetcpa/offers/info/edit.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/actions/', methods=['GET', 'POST'])
def offers_info_actions(id):
	offer = rc.offers.get_try_requested(id, g.user.id) if g.user.is_affiliate else rc.offers.get_by_id(id)
	for suboffer in offer.suboffers:
		suboffer.form = forms.SubOfferForm(request.form, obj=suboffer)
	
	form = forms.SubOfferForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return render_template('cabinetcpa/offers/info/actions.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/actions/edit', methods=['GET', 'POST'])
@advertiser_only
def offers_info_actions_main_edit(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
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
	return render_template('cabinetcpa/offers/info/actions-edit.html', **locals())

@bp.route('/offers/<int:id>/actions/<int:sid>/edit', methods=['GET', 'POST'])
@advertiser_only
def offers_info_actions_edit(id, sid):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	suboffer = None
	for sub in offer.all_suboffers:
		if sub.id == sid: suboffer = sub
	if not suboffer: abort(404)
	form = forms.SubOfferForm(request.form, obj=suboffer)
	form.offer_id = suboffer.id
	if request.method == 'POST' and form.validate():
		form.populate_obj(suboffer)
		if suboffer.updated():
			print suboffer.updated_values()
			rc.offers.update_suboffer(offer.id, suboffer)
			flash(u'Действие успешно изменено', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.offers_info_actions', id=offer.id))
	return render_template('cabinetcpa/offers/info/actions-edit.html', **locals())

@bp.route('/offers/<int:id>/materials', methods=['GET', 'POST'])
def offers_info_materials(id):
	offer = rc.offers.get_try_requested(id, g.user.id) if g.user.is_affiliate else rc.offers.get_by_id(id)
	for banner in offer.banners:
		banner.form = forms.OfferBannerUrlForm(obj=banner)
	form = forms.OfferBannerForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		banner = Banner()
		form.populate_obj(banner)
		image_base64 = base64.encodestring(request.files['image'].stream.read())
		rc.offers.add_banner(offer.id, banner, image_base64)
		flash(u'Баннер успешно загружен', 'success')
		return redirect(request.url)
	return render_template('cabinetcpa/offers/info/materials.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/materials/<int:bid>/delete')
@advertiser_only
def offers_info_materials_delete(id, bid):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	if not offer.banner_by_id(bid): abort(404)
	rc.offers.delete_banner(id, bid)
	flash(u'Баннер удален', 'success')
	return redirect(url_for('.offers_info_materials', id=id))

@bp.route('/offers/<int:id>/materials/<int:bid>', methods=['POST'])
@advertiser_only
def offers_info_materials_update(id, bid):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	banner = offer.banner_by_id(bid) or abort(404)
	form = forms.OfferBannerUrlForm(request.form, obj=banner)
	if request.method == 'POST' and form.validate():
		form.populate_obj(banner)
		rc.offers.update_banner(id, banner)
		flash(u'Баннер успешно изменен', 'success')
	return redirect(url_for('.offers_info_materials', id=id))

@bp.route('/offers/<int:id>/materials/up/', methods=['GET', 'POST'])
@advertiser_only
def offers_info_materials_upload(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
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
	return render_template('cabinetcpa/offers/info/materials-upload.html', offer=offer)

@bp.route('/offers/<int:id>/requests', methods=['GET', 'POST'])
@advertiser_only
def offers_info_requests(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	
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
	grants, count = rc.offer_grants.list(offer_id=offer.id, offset=offset, limit=limit, full=False, **filter_args)
	pages = paginate(page, count, per_page)
	
	form = forms.OfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		if grant and grant.offer.id == offer.id and not grant.blocked:
			action = form.action.data
			if action == 'approve' and not grant.approved:
				rc.offer_grants.approve(grant.id)
				mail.user_grant_approved(grant.offer, grant.affiliate)
				flash(u'Заявка утверждена', 'success')
			elif action == 'reject' and not grant.rejected:
				rc.offer_grants.reject(grant.id, form.reason.data)
				mail.user_grant_rejected(grant.offer, grant.affiliate, form.reason.data)
				flash(u'Заявка отклонена', 'success')
			return redirect(request.url)
	return render_template('cabinetcpa/offers/info/requests.html', offer=offer, grants=grants, pages=pages, form=form)

@bp.route('/offers/<int:id>/settings', methods=['GET', 'POST'])
@affiliate_only
def offers_info_settings(id):
	offer = rc.offers.get_try_requested(id, g.user.id)
	grant = offer.grant
	if not grant or not grant.approved: abort(403)
	form = forms.OfferGrantForm(request.form, obj=grant)
	if request.method == 'POST' and form.validate():
		form.populate_obj(grant)
		if grant.updated():
			rc.offer_grants.update(grant)
			flash(u'Настройки успешно обновлены', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(request.url)
	return render_template('cabinetcpa/offers/info/settings.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/balance', methods=['GET', 'POST'])
@advertiser_only
def offers_info_balance(id):
	offer = rc.offers.get_by_id(id)
	if not offer.owned_by(g.user): abort(403)
	form_in = forms.BalanceForm()
	form_out = forms.BalanceForm()
	if request.method == 'POST':
		type = request.form.get('type', '')
		if type == 'in':
			form_in = forms.BalanceForm(request.form)
			if form_in.validate() and g.user.account.balance >= form_in.amount.data:
				rc.offers.add_to_balance(offer.id, form_in.amount.data)
				flash(u'Счет оффера успешно пополнен', 'success')
				return redirect(url_for('.offers_info', id=offer.id))
		elif type == 'out':
			form_out = forms.BalanceForm(request.form)
			if form_out.validate() and offer.account.balance >= form_out.amount.data:
				rc.offers.remove_from_balance(offer.id, form_out.amount.data)
				flash(u'Средства успешно выведены со счета оффера', 'success')
				return redirect(url_for('.offers_info', id=offer.id))
		else:
			flash(u'Ошибка операции со счетом', 'error')
			return redirect(url_for('.offers_info', id=offer.id))	
	return render_template('cabinetcpa/offers/info/balance.html', offer=offer, form_in=form_in, form_out=form_out)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	offer = rc.offers.get_try_requested(id, g.user.id) if g.user.is_affiliate else rc.offers.get_by_id(id)
	return render_template('cabinetcpa/offers/info/stats.html', offer=offer)

