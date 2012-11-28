# -*- coding: utf-8 -*-
from flask import g, request, flash, redirect, url_for, abort, jsonify, send_file
from heymoose import app, signals, resource as rc
from heymoose.forms import forms
from heymoose.data.models import SubOffer, Banner
from heymoose.data.enums import OfferGrantState
from heymoose.views import excel
from heymoose.views.decorators import template, context, sorted, paginated
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import permission_required
import base64

OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
OFFER_REQUESTS_PER_PAGE = app.config.get('OFFER_REQUESTS_PER_PAGE', 20)
OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
OFFER_ACTIONS_PER_PAGE = app.config.get('OFFER_ACTIONS_PER_PAGE', 20)
OFFER_BANNERS_PER_PAGE = app.config.get('OFFER_BANNERS_PER_PAGE', 20)
AFFILIATE_STATS_PER_PAGE = app.config.get('AFFILIATE_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)
SUBOFFER_STATS_PER_PAGE = app.config.get('SUBOFFER_STATS_PER_PAGE', 20)
DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)

offer_context = context(lambda id, **kwargs: dict(offer=rc.offers.get_by_id(id)))


@bp.route('/offers/')
@template('admin/offers/list.html')
@paginated(OFFERS_PER_PAGE)
def offers_list(**kwargs):
	form = forms.AdminOfferFilterForm(request.args)
	kwargs.update(form.backend_args())
	offers, count = rc.offers.list(**kwargs) if form.validate() else ([], 0)
	return dict(offers=offers, count=count, form=form)

@bp.route('/offers/requests', methods=['GET', 'POST'])
@template('admin/offers/requests.html')
@permission_required('view_offer_requests')
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

	if request.args.get('format') == 'xls':
		grants, _ = rc.offer_grants.list(full=True, offset=0, limit=999999, **filter_args)
		return send_file(excel.grants_to_xls(grants), as_attachment=True, attachment_filename='requests.xls')

	kwargs.update(filter_args)
	grants, count = rc.offer_grants.list(full=True, **kwargs)
	form = forms.AdminOfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		signal_args = dict(grant=grant, notify=form.notify.data, reason=form.reason.data)
		action = form.action.data
		if action == 'unblock':
			rc.offer_grants.unblock(grant.id)
			signals.grant_approved.send(app, **signal_args)
			flash(u'Заявка разблокирована', 'success')
		elif action == 'block':
			rc.offer_grants.block(grant.id, form.reason.data)
			signals.grant_blocked.send(app, **signal_args)
			flash(u'Заявка заблокирована', 'success')
		elif action == 'approve' and not grant.approved:
			rc.offer_grants.approve(grant.id)
			signals.grant_approved.send(app, **signal_args)
			flash(u'Заявка утверждена', 'success')
		elif action == 'reject' and not grant.rejected:
			rc.offer_grants.reject(grant.id, form.reason.data)
			signals.grant_rejected.send(app, **signal_args)
			flash(u'Заявка отклонена', 'success')
		return redirect(request.url)
	return dict(grants=grants, count=count, form=form)

@bp.route('/offers/categories/', methods=['GET', 'POST'])
@template('admin/offers/categories.html')
@permission_required('view_offer_categories')
def offers_categories():
	groups = rc.categories.list_groups()
	form = forms.CategoryForm(request.form)
	form.group.set_groups(groups)
	for group in groups:
		group.form = forms.CategoryForm(group=0, name=group.name)
		group.form.group.set_groups(groups)
		for category in group.categories:
			category.form = forms.CategoryForm(group=group.id, name=category.name)
			category.form.group.set_groups(groups, empty=None)
	if request.method == 'POST' and form.validate():
		if form.group.data:
			rc.categories.add(form.name.data, form.group.data)
		else:
			rc.categories.add_group(form.name.data)
		flash(u'Категория успешно добавлена', 'success')
		return redirect(request.url)
	return dict(form=form, groups=groups)

@bp.route('/offers/categories/<int:id>/', methods=['POST'])
@permission_required('view_offer_categories', post=True)
def offers_categories_update(id):
	groups = rc.categories.list_groups()
	form = forms.CategoryForm(request.form)
	form.group.set_groups(groups, empty=None)
	if form.validate():
		rc.categories.update(id, form.name.data, form.group.data)
		flash(u'Категория успешно изменена', 'success')
	else:
		flash(u'Ошибка изменения категории', 'danger')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/groups/<int:id>/', methods=['POST'])
@permission_required('view_offer_categories', post=True)
def offers_categories_update_group(id):
	groups = rc.categories.list_groups()
	form = forms.CategoryForm(request.form)
	form.group.set_groups(groups)
	if form.validate():
		rc.categories.update_group(id, form.name.data)
		flash(u'Категория успешно изменена', 'success')
	else:
		flash(u'Ошибка изменения категории', 'danger')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/<int:id>/delete', methods=['POST'])
@permission_required('view_offer_categories', post=True)
def offers_categories_delete(id):
	rc.categories.remove(id)
	flash(u'Категория удалена', 'success')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/categories/groups/<int:id>/delete', methods=['POST'])
@permission_required('view_offer_categories', post=True)
def offers_categories_delete_group(id):
	rc.categories.remove_group(id)
	flash(u'Категория удалена', 'success')
	return redirect(url_for('.offers_categories'))

@bp.route('/offers/<int:id>', methods=['GET', 'POST'])
@template('admin/offers/info/info.html')
@offer_context
@permission_required('do_offer_block', post=True)
def offers_info(id, offer):
	offer.overall_debt = rc.withdrawals.overall_debt(offer_id=offer.id)
	form = forms.OfferBlockForm(request.form)
	if request.method == 'POST' and form.validate():
		grants, _ = rc.offer_grants.list(offer_id=offer.id, state=OfferGrantState.APPROVED, blocked=False, offset=0, limit=999999)
		affiliates = [grant.affiliate for grant in grants]
		signal_args = dict(offer=offer, admin=g.user, affiliates=affiliates, reason=form.reason.data,
			notify_affiliates=form.notify.data, notify_advertiser=form.notify.data)
		action = request.form.get('action')
		if action == 'block':
			rc.offers.block(offer.id, form.reason.data)
			signals.offer_blocked.send(app, **signal_args)
			flash(u'Оффер заблокирован', 'success')
		elif action == 'unblock':
			rc.offers.unblock(offer.id)
			signals.offer_unblocked.send(app, **signal_args)
			flash(u'Оффер разблокирован', 'success')
		return redirect(request.url)
	return dict(form=form)

@bp.route('/offers/<int:id>/edit', methods=['GET', 'POST'])
@template('admin/offers/info/edit.html')
@offer_context
@permission_required('do_offer_edit')
def offers_info_edit(id, offer):
	form = forms.AdminOfferEditForm(request.form, obj=offer)
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
@template('admin/offers/info/actions.html')
@offer_context
@permission_required('do_offer_edit', post=True)
def offers_info_actions(id, offer):
	if offer.is_product_offer: abort(403)
	form = forms.SubOfferForm(request.form)
	if request.method == 'POST' and form.validate():
		suboffer = SubOffer()
		form.populate_obj(suboffer)
		rc.offers.add_suboffer(id, suboffer)
		flash(u'Действие успешно добавлено', 'success')
		return redirect(request.url)
	return dict(form=form)

@bp.route('/offers/<int:id>/actions/edit', methods=['GET', 'POST'])
@template('admin/offers/info/actions-edit.html')
@offer_context
@permission_required('do_offer_edit')
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

@bp.route('/offers/<int:id>/actions/<int:sid>/edit', methods=['GET', 'POST'])
@template('admin/offers/info/actions-edit.html')
@offer_context
@permission_required('do_offer_edit')
def offers_info_actions_edit(id, sid, offer):
	if offer.is_product_offer: abort(403)
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
	return dict(suboffer=suboffer, form=form)


@bp.route('/offers/<int:id>/materials/', methods=['GET', 'POST'])
@template('admin/offers/info/materials.html')
@offer_context
@permission_required('do_offer_edit', post=True)
@paginated(OFFER_BANNERS_PER_PAGE)
def offers_info_materials(id, offer, **kwargs):
	form = forms.OfferBannerForm(request.form)
	if request.method == 'POST':
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
	return dict(banners=banners, count=count, form=form)

@bp.route('/offers/<int:id>/materials/up/', methods=['GET', 'POST'])
@template('admin/offers/info/materials-upload.html')
@offer_context
@permission_required('do_offer_edit')
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


@bp.route('/offers/<int:id>/requests', methods=['GET', 'POST'])
@template('admin/offers/info/requests.html')
@offer_context
@permission_required('view_offer_requests')
@paginated(OFFER_REQUESTS_PER_PAGE)
def offers_info_requests(id, offer, **kwargs):
	filter_args = {
		None: dict(),
		'new': dict(blocked=True, moderation=True),
		'blocked': dict(blocked=True, moderation=False),
		'unblocked': dict(blocked=False),
		'moderation': dict(state=OfferGrantState.MODERATION, blocked=False),
		'approved': dict(state=OfferGrantState.APPROVED, blocked=False),
		'rejected': dict(state=OfferGrantState.REJECTED, blocked=False),
	}.get(request.args.get('filter', None), dict())

	if request.args.get('format') == 'xls':
		grants, _ = rc.offer_grants.list(offer_id=offer.id, full=True, offset=0, limit=999999, **filter_args)
		return send_file(excel.grants_to_xls(grants), as_attachment=True, attachment_filename='requests.xls')
	
	kwargs.update(filter_args)
	grants, count = rc.offer_grants.list(offer_id=offer.id, full=True, **kwargs)
	form = forms.AdminOfferRequestDecisionForm(request.form)
	if request.method == 'POST' and form.validate():
		grant = rc.offer_grants.get_by_id(form.grant_id.data, full=True)
		if grant and grant.offer.id == offer.id:
			signal_args = dict(grant=grant, notify=form.notify.data, reason=form.reason.data)
			action = form.action.data
			if action == 'unblock':
				rc.offer_grants.unblock(grant.id)
				signals.grant_approved.send(app, **signal_args)
				flash(u'Заявка разблокирована', 'success')
			elif action == 'block':
				rc.offer_grants.block(grant.id, form.reason.data)
				signals.grant_blocked.send(app, **signal_args)
				flash(u'Заявка заблокирована', 'success')
			elif action == 'approve' and not grant.approved:
				rc.offer_grants.approve(grant.id)
				signals.grant_approved.send(app, **signal_args)
				flash(u'Заявка утверждена', 'success')
			elif action == 'reject' and not grant.rejected:
				rc.offer_grants.reject(grant.id, form.reason.data)
				signals.grant_rejected.send(app, **signal_args)
				flash(u'Заявка отклонена', 'success')
			return redirect(request.url)
	return dict(grants=grants, count=count, form=form)

@bp.route('/offers/<int:id>/sales/', methods=['GET', 'POST'])
@template('admin/offers/info/sales.html')
@offer_context
@permission_required('view_offer_sales')
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

@bp.route('/offers/<int:id>/finances/', methods=['GET', 'POST'])
@template('admin/offers/info/finances.html')
@offer_context
@permission_required('view_offer_finances')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def offers_info_finances(id, offer, **kwargs):
	form = forms.DebtFilterForm(request.args)
	if request.method == 'POST':
		if form.validate():
			rc.withdrawals.withdraw(
				offer_id=offer.id,
				user_id=request.form.getlist('user_id'),
				basis=request.form.getlist('basis'),
				amount=request.form.getlist('amount'),
				**form.backend_args()
			)
			flash(u'Выплаты успешно выполнены', 'success')
		else:
			flash(u'Ошибка при совершении выплат', 'danger')
		return redirect(request.url)
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debts(offer_id=offer.id, **kwargs)
		overall_debt = rc.withdrawals.overall_debt(offer_id=offer.id, **kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(debts=debts, count=count, overall_debt=overall_debt, form=form)


@bp.route('/offers/<int:id>/operations/', methods=['GET', 'POST'])
@template('admin/offers/info/operations.html')
@offer_context
@permission_required('view_offer_operations')
def offers_info_operations(id, offer):
	if request.method == 'POST' and 'csv' in request.files:
		transactions = [t.strip() for t in request.files['csv'].read().split()]
		if 'approve' in request.form:
			count = rc.actions.approve_by_transactions(offer.id, transactions)
			flash(u'Подтверждено {0} действий'.format(count), 'success')
		elif 'cancel' in request.form:
			count = rc.actions.cancel_by_transactions(offer.id, transactions)
			flash(u'Отменено {0} действий'.format(count), 'success')
		return redirect(request.url)
	return dict()


@bp.route('/offers/<int:id>/stats/affiliate')
@template('admin/offers/info/stats/affiliate.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('clicks_count', 'desc')
@paginated(AFFILIATE_STATS_PER_PAGE)
def offers_info_stats_affiliate(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_affiliate_by_offer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/referer')
@template('admin/offers/info/stats/referer.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('clicks_count', 'desc')
@paginated(REFERER_STATS_PER_PAGE)
def offers_info_stats_referer(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_referer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/keywords')
@template('admin/offers/info/stats/keywords.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('clicks_count', 'desc')
@paginated(KEYWORDS_STATS_PER_PAGE)
def offers_info_stats_keywords(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/suboffer')
@template('admin/offers/info/stats/suboffer.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/offers/<int:id>/stats/suboffer/affiliate')
@template('admin/offers/info/stats/suboffer.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_affiliate(id, offer, **kwargs):
	affiliate = rc.users.get_by_id(request.args.get('aff_id'))
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(offer_id=offer.id, aff_id=affiliate.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, affiliate=affiliate)

@bp.route('/offers/<int:id>/stats/suboffer/referer')
@template('admin/offers/info/stats/suboffer.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_referer(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(referer=request.args.get('referer'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_referer(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count)

@bp.route('/offers/<int:id>/stats/suboffer/keywords')
@template('admin/offers/info/stats/suboffer.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def offers_info_stats_suboffer_keywords(id, offer, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(keywords=request.args.get('keywords'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_keywords(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count)


@bp.route('/offers/<int:id>/stats/fraud')
@template('admin/offers/info/stats/fraud.html')
@offer_context
@permission_required('view_offer_stats')
@sorted('rate', 'desc')
@paginated(AFFILIATE_STATS_PER_PAGE)
def offers_info_stats_fraud(id, offer, **kwargs):
	form = forms.UserFilterForm(request.args)
	kwargs.update(form.backend_args())
	user_stats, count = rc.user_stats.list_fraud(offer_id=offer.id, **kwargs) if form.validate() else ([], 0)
	return dict(user_stats=user_stats, count=count, form=form)
