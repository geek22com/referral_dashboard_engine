# -*- coding: utf-8 -*-
from flask import render_template, g, request, redirect, flash, url_for, session, send_file
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.views import excel
from heymoose.views.decorators import template, sorted, paginated
from heymoose.utils.pagination import current_page, page_limits, paginate as paginate2
from heymoose.utils.convert import to_unixtime
from heymoose.forms import forms
from heymoose.db.models import UserInfo
from heymoose.data.enums import Roles
from heymoose.mail import marketing as mmail
from heymoose.mail import transactional as tmail

USERS_PER_PAGE = app.config.get('USERS_PER_PAGE', 20)
ACCOUNTING_ENTRIES_PER_PAGE = app.config.get('ACCOUNTING_ENTRIES_PER_PAGE', 20)
OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
SUB_ID_STATS_PER_PAGE = app.config.get('SUB_ID_STATS_PER_PAGE', 20)
SOURCE_ID_STATS_PER_PAGE = app.config.get('SOURCE_ID_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)
SUBOFFER_STATS_PER_PAGE = app.config.get('SUBOFFER_STATS_PER_PAGE', 20)
DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)


@bp.route('/users/')
@template('admin/users.html')
@paginated(USERS_PER_PAGE)
def users_list(**kwargs):
	filter_args = {
		None: dict(),
		'advertisers': dict(role=Roles.ADVERTISER),
		'affiliates': dict(role=Roles.AFFILIATE),
		'admins': dict(role=Roles.ADMIN)
	}.get(request.args.get('filter', None), dict())
	if request.args.get('format', '') == 'xls':
		users = rc.users.list(offset=0, limit=9999999, **filter_args)
		users.reverse()
		user_infos = { user_info.user_id : user_info for user_info in  UserInfo.query.all() }
		for user in users: user.info = user_infos.get(user.id, None)
		return send_file(excel.users_to_xls(users), as_attachment=True, attachment_filename='users.xls')
	kwargs.update(filter_args)
	users = rc.users.list(full=True, **kwargs)
	count = rc.users.count(**kwargs)
	return dict(users=users, count=count)

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

@bp.route('/users/<int:id>/login')
def users_info_login(id):
	session['user_id'] = id
	session.permanent = False
	return redirect(url_for('site.gateway'))

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

@bp.route('/users/<int:id>/balance/', methods=['GET', 'POST'])
@template('admin/users-info-balance.html')
@paginated(ACCOUNTING_ENTRIES_PER_PAGE)
def users_info_balance(id, **kwargs):
	user = rc.users.get_by_id(id)
	form = forms.BalanceForm(request.form)
	entries, count = rc.accounts.entries_list(user.account.id, **kwargs)
	if user.is_advertiser and request.method == 'POST' and form.validate():
		rc.users.add_to_customer_account(user.id, round(form.amount.data, 2))
		flash(u'Баланс успешно пополнен', 'success')
		return redirect(request.url)
	return dict(user=user, entries=entries, count=count, form=form)

@bp.route('/users/<int:id>/finances/')
@template('admin/users-info-finances.html')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def users_info_finances(id, **kwargs):
	user = rc.users.get_by_id(id)
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debt_by_offer(aff_id=user.id, **kwargs)
		overall_debt = rc.withdrawals.overall_debt(aff_id=user.id, **kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(user=user, debts=debts, count=count, overall_debt=overall_debt, form=form)

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
	form = forms.CabinetSubIdStatsForm(request.args)
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
	form = forms.CabinetStatsForm(request.args)
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
	form = forms.CabinetStatsForm(request.args)
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
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, form=form)

@bp.route('/users/<int:id>/stats/suboffer')
@template('admin/users-info-stats-suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, offer=form.offer.selected)

@bp.route('/users/<int:id>/stats/suboffer/sub_id')
@template('admin/users-info-stats-suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_sub_id(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	kwargs.update(form.sub_ids_from_string(request.args.get('sub_ids')))
	stats, count = rc.offer_stats.list_suboffer_by_sub_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, offer=form.offer.selected)

@bp.route('/users/<int:id>/stats/suboffer/source_id')
@template('admin/users-info-stats-suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_source_id(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(source_id=request.args.get('source_id'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_source_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, offer=form.offer.selected)

@bp.route('/users/<int:id>/stats/suboffer/referer')
@template('admin/users-info-stats-suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_referer(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(referer=request.args.get('referer'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_referer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, offer=form.offer.selected)

@bp.route('/users/<int:id>/stats/suboffer/keywords')
@template('admin/users-info-stats-suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_keywords(id, **kwargs):
	user = rc.users.get_by_id(id)
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(keywords=request.args.get('keywords'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_keywords(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(user=user, stats=stats, count=count, offer=form.offer.selected)