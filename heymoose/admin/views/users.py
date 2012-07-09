# -*- coding: utf-8 -*-
from flask import render_template, g, request, redirect, flash, url_for
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.views.decorators import template, sorted, paginated
from heymoose.utils import pagination
from heymoose.utils.pagination import current_page, page_limits, paginate as paginate2
from heymoose.utils.shortcuts import paginate
from heymoose.utils.convert import to_unixtime
from heymoose.forms import forms
from heymoose.data.enums import Roles
from heymoose.mail import marketing as mmail
from heymoose.mail import transactional as tmail

OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
SUB_ID_STATS_PER_PAGE = app.config.get('SUB_ID_STATS_PER_PAGE', 20)
SOURCE_ID_STATS_PER_PAGE = app.config.get('SOURCE_ID_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)


@bp.route('/users/')
def users_list():
	filter_args = {
		None: dict(),
		'advertisers': dict(role=Roles.ADVERTISER),
		'affiliates': dict(role=Roles.AFFILIATE),
		'admins': dict(role=Roles.ADMIN)
	}.get(request.args.get('filter', None), dict())
	
	page = current_page()
	count = rc.users.count(**filter_args)
	per_page = app.config.get('USERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	users = rc.users.list(offset=offset, limit=limit, full=True, **filter_args)
	return render_template('admin/users.html', users=users, pages=pages, count=count)

@bp.route('/users/<int:id>', methods=['GET', 'POST'])
def users_info(id):
	user = rc.users.get_by_id(id)
	form = forms.UserBlockForm(request.form)
	if request.method == 'POST':
		if not user.blocked and form.validate():
			rc.users.block(user.id, form.reason.data)
			if form.mail.data:
				tmail.user_blocked(user, form.reason.data)
			tmail.admin_user_blocked(user, g.user, form.reason.data)
			flash(u'Учетная запись заблокирована', 'success')
			return redirect(url_for('.users_info', id=user.id))
		elif user.blocked:
			rc.users.unblock(user.id)
			flash(u'Учетная запись разблокирована', 'success')
			return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info.html', user=user, form=form)

@bp.route('/users/<int:id>/offers')
def users_info_offers(id):
	user = rc.users.get_by_id(id)
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	if user.is_advertiser:
		offers, count = rc.offers.list(offset=offset, limit=limit, advertiser_id=user.id)
	else:
		offers, count = rc.offers.list_requested(user.id, offset=offset, limit=limit)
	pages = paginate2(page, count, per_page)
	return render_template('admin/users-info-offers.html', user=user, offers=offers, pages=pages)

@bp.route('/users/<int:id>/stats')
def users_info_stats(id):
	user = rc.users.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 10)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_user(user, offset=offset, limit=limit,
			**{'from' : to_unixtime(form.dt_from.data, True), 'to' : to_unixtime(form.dt_to.data, True)})
		pages = paginate2(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('admin/users-info-stats.html', user=user, stats=stats, pages=pages, form=form)

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def users_info_edit(id):
	user = rc.users.get_by_id(id)
	FormClass = forms.AdminAdvertiserEditForm if user.is_advertiser else forms.AdminAffiliateEditForm
	form = FormClass(request.form, obj=user)	
	if request.method == 'POST' and form.validate():
		form.populate_obj(user)
		if user.updated():
			rc.users.update(user)
			flash(u'Профиль пользователя успешно изменен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info-edit.html', user=user, form=form)

@bp.route('/users/<int:id>/password', methods=['GET', 'POST'])
def users_info_password_change(id):
	user = rc.users.get_by_id(id)
	form = forms.AdminPasswordChangeForm(request.form)
	if request.method == 'POST' and form.validate():
		form.populate_obj(user)
		rc.users.update(user)
		flash(u'Пароль пользователя успешно изменен', 'success')
		return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info-password-change.html', user=user, form=form)

@bp.route('/users/<int:id>/a/lists/add')
def users_info_lists_add(id):
	user = rc.users.get_by_id(id)
	if mmail.lists_add_user(user, mail_if_failed=False):
		flash(u'Пользователь добавлен в списки рассылки', 'success')
	else:
		flash(u'Ошибка при добавлении пользователя в списки рассылки', 'error')
	return redirect(url_for('.users_info', id=user.id))

@bp.route('/users/<int:id>/balance', methods=['GET', 'POST'])
def users_info_balance(id):
	user = rc.users.get_by_id(id)
	delete_form = forms.WithdrawalDeleteForm()
	
	if user.is_advertiser:
		withdrawals = None
		form = forms.BalanceForm(request.form)
		if request.method == 'POST' and form.validate():
			rc.users.add_to_customer_account(user.id, round(form.amount.data, 2))
			flash(u'Баланс успешно пополнен', 'success')
			return redirect(request.url)
	elif user.is_affiliate:
		withdrawals = rc.accounts.withdrawals_list(user.account.id)
		form = forms.BalanceForm(request.form, amount=user.account.balance)
		if request.method == 'POST' and form.validate():
			rc.accounts.make_withdrawal(user.account.id, round(form.amount.data, 2))
			flash(u'Выплата успешно создана', 'success')
			return redirect(request.url)
	else:
		flash(u'Пользователь не имеет счета', 'error')
		return redirect(url_for('.users_info', id=user.id))
	
	page = pagination.current_page()
	per_page = app.config.get('ACCOUNTING_ENTRIES_PER_PAGE', 20)
	offset, limit = pagination.page_limits(page, per_page)
	entries, count = rc.accounts.entries_list(user.account.id, offset=offset, limit=limit)
	pages = pagination.paginate(page, count, per_page)
	
	return render_template('admin/users-info-balance.html', entries=entries,
		withdrawals=withdrawals, pages=pages, user=user, form=form, delete_form=delete_form)
	
@bp.route('/users/<int:id>/balance/withdrawals/<int:wid>/approve', methods=['POST'])
def users_info_approve_withdrawal(id, wid):
	user = rc.users.get_by_id(id)
	rc.accounts.approve_withdrawal(user.account.id, wid)
	flash(u'Выплата подтверждена', 'success')
	return redirect(url_for('.users_info_balance', id=user.id))

@bp.route('/users/<int:id>/balance/withdrawals/<int:wid>/delete', methods=['POST'])
def users_info_delete_withdrawal(id, wid):
	user = rc.users.get_by_id(id)
	form = forms.WithdrawalDeleteForm(request.form)
	if form.validate():
		rc.accounts.delete_withdrawal(user.account.id, wid, form.reason.data)
		flash(u'Выплата разработчику отменена', 'success')
	else:
		flash(u'При выплате разработчику произошла ошибка', 'error')
	return redirect(url_for('.users_info_balance', id=user.id))

@bp.route('/users/<int:id>/stats/offer')
@template('admin/users-info-stats-offer.html')
@sorted('clicks_count', 'desc')
@paginated(OFFER_STATS_PER_PAGE)
def users_info_stats_offer(id, **kwargs):
	user = rc.users.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_user(user, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)

@bp.route('/users/<int:id>/stats/subid')
@template('admin/users-info-stats-sub-id.html')
@sorted('clicks_count', 'desc')
@paginated(SUB_ID_STATS_PER_PAGE)
def users_info_stats_sub_id(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_sub_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)

@bp.route('/users/<int:id>/stats/sourceid')
@template('admin/users-info-stats-source-id.html')
@sorted('clicks_count', 'desc')
@paginated(SOURCE_ID_STATS_PER_PAGE)
def users_info_stats_source_id(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_source_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)

@bp.route('/users/<int:id>/stats/referer')
@template('admin/users-info-stats-referer.html')
@sorted('clicks_count', 'desc')
@paginated(REFERER_STATS_PER_PAGE)
def users_info_stats_referer(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_referer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)

@bp.route('/users/<int:id>/stats/keywords')
@template('admin/users-info-stats-keywords.html')
@sorted('clicks_count', 'desc')
@paginated(KEYWORDS_STATS_PER_PAGE)
def users_info_stats_keywords(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)
