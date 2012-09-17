# -*- coding: utf-8 -*-
from flask import request, flash, redirect, url_for, abort, jsonify, send_file
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.models import SubOffer, Banner
from heymoose.data.enums import OfferGrantState
from heymoose.notifications import notify
from heymoose.views import excel
from heymoose.views.decorators import template, sorted, paginated
from heymoose.admin import blueprint as bp
import base64

OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
OFFER_REQUESTS_PER_PAGE = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
OFFER_ACTIONS_PER_PAGE = app.config.get('OFFER_ACTIONS_PER_PAGE', 20)
AFFILIATE_STATS_PER_PAGE = app.config.get('AFFILIATE_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)
SUBOFFER_STATS_PER_PAGE = app.config.get('SUBOFFER_STATS_PER_PAGE', 20)
DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)

@bp.route('/offers/')
@template('admin/offers/list.html')
@paginated(OFFERS_PER_PAGE)
def offers_list(**kwargs):
	form = forms.OfferFilterForm(request.args)
	kwargs.update(form.backend_args())
	offers, count = rc.offers.list(**kwargs) if form.validate() else ([], 0)
	return dict(offers=offers, count=count, form=form)

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
			if form.notify.data and grant.approved: notify.grant_approved(grant)
			flash(u'Заявка разблокирована', 'success')
		elif action == 'block':
			rc.offer_grants.block(grant.id, form.reason.data)
			if form.notify.data: notify.grant_blocked(grant, form.reason.data)
			flash(u'Заявка заблокирована', 'success')
		elif action == 'approve' and not grant.approved:
			rc.offer_grants.approve(grant.id)
			if form.notify.data and not grant.blocked: notify.grant_approved(grant)
			flash(u'Заявка утверждена', 'success')
		elif action == 'reject' and not grant.rejected:
			rc.offer_grants.reject(grant.id, form.reason.data)
			if form.notify.data: notify.grant_rejected(grant, form.reason.data)
			flash(u'Заявка отклонена', 'success')
		return redirect(request.url)
	return dict(grants=grants, count=count, form=form)

@bp.route('/offers/categories/', methods=['GET', 'POST'])
@template('admin/offers/categories.html')
def offers_categories():
	form = forms.CategoryForm(request.form)
	groups = form.group.groups
	for group in groups:
		group.form = forms.CategoryForm(group=0, name=group.name)
		for category in group.categories:
			category.form = forms.CategoryEditForm(group=group.id, name=category.name)
	if request.method == 'POST' and form.validate():
		if form.group.data:
			rc.categories.add(form.name.data, form.group.data)
		else:
			rc.categories.add_group(form.name.data)
		flash(u'Категория успешно добавлена', 'success')
		return redirect(request.url)
	return dict(form=form, groups=groups)

@bp.route('/offers/categories/<int:id>/', methods=['POST'])
def offers_categories_update(id):
	form = forms.CategoryEditForm(request.form)
	if form.validate():
		rc.categories.update(id, form.name.data, form.group.data)
		flash(u'Категория успешно изменена', 'success')
	else:
		flash(u'Ошибка изменения категории', 'danger')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/groups/<int:id>/', methods=['POST'])
def offers_categories_update_group(id):
	form = forms.CategoryForm(request.form)
	if form.validate():
		rc.categories.update_group(id, form.name.data)
		flash(u'Категория успешно изменена', 'success')
	else:
		flash(u'Ошибка изменения категории', 'danger')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/<int:id>/delete', methods=['POST'])
def offers_categories_delete(id):
	rc.categories.remove(id)
	flash(u'Категория удалена', 'success')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/groups/<int:id>/delete', methods=['POST'])
def offers_categories_delete_group(id):
	rc.categories.remove_group(id)
	flash(u'Категория удалена', 'success')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
@template('admin/offers/info/info.html')
def offers_info(id):
	offer = rc.offers.get_by_id(id)
	form = forms.OfferBlockForm(request.form)
	if request.method == 'POST' and form.validate():
		action = request.form.get('action')
		if action == 'block':
			rc.offers.block(offer.id, form.reason.data)
			if form.notify.data: notify.offer_blocked(offer, form.reason.data)
			flash(u'Оффер заблокирован', 'success')
		elif action == 'unblock':
			rc.offers.unblock(offer.id)
			if form.notify.data: notify.offer_unblocked(offer)
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
	if offer.exclusive: abort(403)
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
@template('admin/offers/info/actions-edit.html')
def offers_info_actions_edit(id, sid):
	offer = rc.offers.get_by_id(id)
	if offer.exclusive: abort(403)
	suboffer = offer.suboffer_by_id(sid)
	if not suboffer: abort(404)
	form = forms.AdminSubOfferEditForm(request.form, obj=suboffer)
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
@template('admin/offers/info/materials.html')
def offers_info_materials(id):
	offer = rc.offers.get_by_id(id)
	form = forms.OfferBannerForm(request.form)
	if request.method == 'POST' and form.validate():
		banner = Banner()
		form.populate_obj(banner)
		image_base64 = base64.encodestring(request.files['image'].stream.read())
		rc.offers.add_banner(offer.id, banner, image_base64)
		flash(u'Баннер успешно загружен', 'success')
		return redirect(request.url)
	return dict(offer=offer, form=form)

@bp.route('/offers/<int:id>/materials/<int:bid>/delete')
def offers_info_materials_delete(id, bid):
	offer = rc.offers.get_by_id(id)
	if not offer.banner_by_id(bid): abort(404)
	rc.offers.delete_banner(id, bid)
	flash(u'Баннер удален', 'success')
	return redirect(url_for('.offers_info_materials', id=id))

@bp.route('/offers/<int:id>/materials/up/', methods=['GET', 'POST'])
@template('admin/offers/info/materials-upload.html')
def offers_info_materials_upload(id):
	offer = rc.offers.get_by_id(id)
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
				if form.notify.data and grant.approved: notify.grant_approved(grant)
				flash(u'Заявка разблокирована', 'success')
			elif action == 'block':
				rc.offer_grants.block(grant.id, form.reason.data)
				if form.notify.data: notify.grant_blocked(grant, form.reason.data)
				flash(u'Заявка заблокирована', 'success')
			elif action == 'approve' and not grant.approved:
				rc.offer_grants.approve(grant.id)
				if form.notify.data and not grant.blocked: notify.grant_approved(grant)
				flash(u'Заявка утверждена', 'success')
			elif action == 'reject' and not grant.rejected:
				rc.offer_grants.reject(grant.id, form.reason.data)
				if form.notify.data: notify.grant_rejected(grant, form.reason.data)
				flash(u'Заявка отклонена', 'success')
			return redirect(request.url)
	return dict(offer=offer, grants=grants, count=count, form=form)

@bp.route('/offers/<int:id>/sales/', methods=['GET', 'POST'])
@template('admin/offers/info/sales.html')
@sorted('creation_time', 'desc')
@paginated(OFFER_ACTIONS_PER_PAGE)
def offers_info_sales(id, **kwargs):
	offer = rc.offers.get_by_id(id)
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

@bp.route('/offers/<int:id>/finances/', methods=['GET', 'POST'])
@template('admin/offers/info/finances.html')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def offers_info_finances(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		if request.method == 'POST':
			rc.withdrawals.withdraw(
				offer_id=offer.id,
				user_id=request.form.getlist('user_id'),
				amount=request.form.getlist('amount'),
				**form.backend_args()
			)
			flash(u'Выплаты успешно выполнены', 'success')
			return redirect(request.url)
		else:
			kwargs.update(form.backend_args())
			debts_list = rc.withdrawals.list_debt_by_affiliate(offer.id, **kwargs)
			count = debts_list.count
	else:
		debts_list, count = [], 0
	return dict(offer=offer, debts_list=debts_list, count=count, form=form)

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

@bp.route('/offers/<int:id>/stats/suboffer')
@template('admin/offers/info/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/suboffer/affiliate')
@template('admin/offers/info/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_affiliate(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	affiliate = rc.users.get_by_id(request.args.get('aff_id'))
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(offer_id=offer.id, aff_id=affiliate.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count, affiliate=affiliate)

@bp.route('/offers/<int:id>/stats/suboffer/referer')
@template('admin/offers/info/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_referer(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(referer=request.args.get('referer'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_referer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count)

@bp.route('/offers/<int:id>/stats/suboffer/keywords')
@template('admin/offers/info/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_keywords(id, **kwargs):
	offer = rc.offers.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(keywords=request.args.get('keywords'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_keywords(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(offer=offer, stats=stats, count=count)
