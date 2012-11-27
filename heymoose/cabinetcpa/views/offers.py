# -*- coding: utf-8 -*-
from flask import request, flash, g, redirect, url_for, abort, jsonify, send_file
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import Offer, OfferGrant, SubOffer, Banner, Placement
from heymoose.data.enums import OfferGrantState
from heymoose.notifications import notify
from heymoose.views import excel
from heymoose.views.decorators import template, context, paginated, sorted
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only, affiliate_only
from heymoose.utils.lang import create_dict
import base64


OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
OFFER_ACTIONS_PER_PAGE = app.config.get('OFFER_ACTIONS_PER_PAGE', 20)
OFFER_BANNERS_PER_PAGE = app.config.get('OFFER_BANNERS_PER_PAGE', 20)
PRODUCTS_PER_PAGE = app.config.get('PRODUCTS_PER_PAGE', 20)

INFINITE_LIMITS = dict(offset=0, limit=999999)


def existing_offer(id):
	return rc.offers.get_by_id(id, aff_id=g.user.id if g.user.is_affiliate else None)

def visible_offer(id):
	'''
	For both advertisers and affiliates. For advertiser returns offer only if it is his offer
	or if this offer is visible (approved, active, launched). For affiliate returns offer only
	if offer is granted for this affiliate or if it is visible. Otherwise returns 404.
	'''
	offer = existing_offer(id)
	if offer.visible or (g.user.is_advertiser and offer.owned_by(g.user)) or (g.user.is_affiliate and offer.placements_count):
		return offer
	abort(404)

def advertiser_offer(id):
	'''
	For advertisers only. Returns offer if it is owned by current advetiser.
	Otherwise returns 404.
	'''
	offer = existing_offer(id)
	if not offer.owned_by(g.user): abort(404)
	return offer

def offer_placement(pid, offer):
	placement = rc.placements.get_by_id(pid)
	if placement.offer != offer: abort(404)
	return placement


offer_context = context(lambda id, **kwargs: dict(offer=existing_offer(id)))
visible_offer_context = context(lambda id, **kwargs: dict(offer=visible_offer(id)))
advertiser_offer_context = context(lambda id, **kwargs: dict(offer=advertiser_offer(id)))
offer_placement_context = context(lambda pid, offer, **kwargs: dict(placement=offer_placement(pid, offer)))


@bp.route('/offers/')
@template('cabinetcpa/offers/all.html')
@paginated(OFFERS_PER_PAGE)
def offers_all(**kwargs):
	form = forms.OfferFilterForm(request.args)
	kwargs.update(form.backend_args())
	offers, count = rc.offers.list(approved=True, active=True, launched=True, **kwargs) if form.validate() else ([], 0)
	return dict(offers=offers, count=count, form=form)


@bp.route('/offers/my/')
@advertiser_only
@template('cabinetcpa/offers/list.html')
@paginated(OFFERS_PER_PAGE)
def offers_list(**kwargs):
	offers, count = rc.offers.list(advertiser_id=g.user.id, **kwargs)
	return dict(offers=offers, count=count)


@bp.route('/offers/requested/')
@affiliate_only
@template('cabinetcpa/offers/requested.html')
@paginated(OFFERS_PER_PAGE)
def offers_requested(**kwargs):
	offers, count = rc.offers.list_requested(g.user.id, **kwargs)
	return dict(offers=offers, count=count)


@bp.route('/offers/products/')
@affiliate_only
@template('cabinetcpa/offers/products.html')
@paginated(PRODUCTS_PER_PAGE)
def offers_products(offset, limit):
	feed_args = create_dict(
		key=g.user.secret_key,
		q=request.args.get('q') or None,
		s=request.args.getlist('s'),
		c=request.args.getlist('c'),
		site=request.args.get('site') or None,
		offset=offset,
		limit=limit
	)
	catalog = rc.products.feed(**feed_args)
	catalog_size = rc.products.feed_size(**feed_args)
	shops = rc.products.categories(g.user.id, site=request.args.get('site'))
	sites = filter(lambda x: x.is_approved, rc.sites.list(aff_id=g.user.id, **INFINITE_LIMITS)[0])
	return dict(catalog=catalog, shops=shops, count=catalog_size, sites=sites, feed_args=feed_args)


@bp.route('/offers/new/', methods=['GET', 'POST'])
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


@bp.route('/offers/<int:id>/', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/info.html')
@visible_offer_context
def offers_info(id, offer):
	offer.overall_debt = rc.withdrawals.overall_debt(offer_id=offer.id)
	return dict()


@bp.route('/offers/<int:id>/edit/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/edit.html')
@advertiser_offer_context
def offers_info_edit(id, offer):
	form = forms.OfferEditForm(request.form, obj=offer)
	if request.method == 'POST' and form.validate():
		form.populate_obj(offer)
		if offer.updated():
			rc.offers.update(offer)
			flash(u'Оффер успешно изменен', 'success')
			return redirect(url_for('.offers_info', id=offer.id))
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
	return dict(form=form)


@bp.route('/offers/<int:id>/actions/', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/actions.html')
@visible_offer_context
def offers_info_actions(id, offer):
	if offer.is_product_offer: abort(403)
	form = forms.SubOfferForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return dict(form=form)


@bp.route('/offers/<int:id>/actions/edit/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/actions-edit.html')
@advertiser_offer_context
def offers_info_actions_main_edit(id, offer):
	if offer.is_product_offer: abort(403)
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
	return dict(suboffer=offer, form=form)


@bp.route('/offers/<int:id>/actions/<int:sid>/edit/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/actions-edit.html')
@advertiser_offer_context
def offers_info_actions_edit(id, sid, offer):
	if offer.is_product_offer: abort(403)
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
	return dict(suboffer=suboffer, form=form)


@bp.route('/offers/<int:id>/materials/', methods=['GET', 'POST'])
@template('cabinetcpa/offers/info/materials.html')
@visible_offer_context
@paginated(OFFER_BANNERS_PER_PAGE)
def offers_info_materials(id, offer, **kwargs):
	form = forms.OfferBannerForm(request.form)
	if offer.owned_by(g.user) and request.method == 'POST':
		if 'id' in request.form:
			rc.banners.remove_by_ids(offer.id, request.form.getlist('id'))
			flash(u'Баннеры успешно удалены', 'success')
	 	elif form.validate():
			banner = Banner()
			form.populate_obj(banner)
			image_base64 = base64.encodestring(request.files['image'].stream.read())
			rc.offers.add_banner(offer.id, banner, image_base64)
			flash(u'Баннер успешно загружен', 'success')
		return redirect(request.url)
	banners, count = rc.banners.list(offer_id=offer.id, **kwargs)
	placements, _ = rc.placements.list(aff_id=g.user.id, offer_id=offer.id, **INFINITE_LIMITS)
	placements = [placement for placement in placements if placement.is_approved]
	return dict(banners=banners, count=count, form=form, placements=placements)


@bp.route('/offers/<int:id>/materials/up/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/materials-upload.html')
@advertiser_offer_context
def offers_info_materials_upload(id, offer):
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
	return dict()


@bp.route('/offers/<int:id>/sales/', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/offers/info/sales.html')
@advertiser_offer_context
@sorted('creation_time', 'desc')
@paginated(OFFER_ACTIONS_PER_PAGE)
def offers_info_sales(id, offer, **kwargs):
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
	return dict(actions=actions, count=count, form=form)


@bp.route('/offers/<int:id>/placements/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/offers/info/placements.html')
@visible_offer_context
def offers_info_placements(id, offer, **kwargs):
	placements, _ = rc.placements.list(aff_id=g.user.id, offer_id=offer.id, **INFINITE_LIMITS)
	existing_site_ids = [placement.site.id for placement in placements]
	sites, _ = rc.sites.list(aff_id=g.user.id, **INFINITE_LIMITS)
	sites = [site for site in sites if site.is_approved and site.id not in existing_site_ids]
	form = forms.PlacementForm(request.form)
	form.site.set_sites(sites, empty=None)
	if request.method == 'POST' and form.validate():
		placement = Placement(affiliate=g.user, offer=offer)
		form.populate_obj(placement)
		rc.placements.add(placement)
		flash(u'Размещение успешно создано', 'success')
		return redirect(request.url)
	return dict(form=form, placements=placements)


@bp.route('/offers/<int:id>/placements/<int:pid>/edit/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/offers/info/placements-edit.html')
@visible_offer_context
@offer_placement_context
def offers_info_placements_edit(id, pid, offer, placement):
	form = forms.PlacementEditForm(request.form, obj=placement)
	if request.method == 'POST' and form.validate():
		form.populate_obj(placement)
		rc.placements.update(placement)
		flash(u'Размещение успешно изменено', 'success')
		return redirect(url_for('.offers_info_placements', id=offer.id))
	return dict(form=form)


@bp.route('/offers/<int:id>/placements/<int:pid>/delete/')
@affiliate_only
@visible_offer_context
@offer_placement_context
def offers_info_placements_delete(id, pid, offer, placement):
	rc.placements.remove(placement)
	flash(u'Размещение удалено', 'success')
	return redirect(url_for('.offers_info_placements', id=offer.id))
