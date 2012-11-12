# -*- coding: utf-8 -*-
from flask import g, request, redirect, flash, url_for, session, send_file
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import permission_required, superadmin_required, not_enough_permissions
from heymoose.views import excel
from heymoose.views.decorators import template, context, sorted, paginated
from heymoose.utils.convert import to_unixtime
from heymoose.forms import forms
from heymoose.data.models import User
from heymoose.data.enums import Roles
from heymoose.data.mongo.models import UserInfo, AdminPermissions
from heymoose.mail import marketing as mmail
from heymoose.mail import transactional as tmail


USERS_PER_PAGE = app.config.get('USERS_PER_PAGE', 20)
OFFERS_PER_PAGE = app.config.get('OFFERS_PER_PAGE', 10)
ACCOUNTING_ENTRIES_PER_PAGE = app.config.get('ACCOUNTING_ENTRIES_PER_PAGE', 20)
OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
SUB_ID_STATS_PER_PAGE = app.config.get('SUB_ID_STATS_PER_PAGE', 20)
SOURCE_ID_STATS_PER_PAGE = app.config.get('SOURCE_ID_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)
SUBOFFER_STATS_PER_PAGE = app.config.get('SUBOFFER_STATS_PER_PAGE', 20)
DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)


def user_context_provider(id):
	user = rc.users.get_by_id(id)
	if user.is_admin and user.id != g.user.id and not g.user.is_superadmin:
		not_enough_permissions()
	return dict(user=user)

def advertiser_trigger(user, **kwargs):
	return user.is_advertiser

def affiliate_trigger(user, **kwargs):
	return user.is_affiliate

def permission_required_on_advertiser(permission, **kwargs):
	return permission_required(permission, trigger=advertiser_trigger, **kwargs)

def permission_required_on_affiliate(permission, **kwargs):
	return permission_required(permission, trigger=affiliate_trigger, **kwargs)


@bp.route('/users/')
@template('admin/users/list.html')
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

@bp.route('/users/register/admin/', methods=['GET', 'POST'])
@superadmin_required()
@template('admin/users/register-admin.html')
def users_register_admin():
	form = forms.AdminRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User()
		form.populate_obj(user)
		rc.users.add(user)
		user = rc.users.get_by_email_safe(user.email)
		if user:
			rc.users.add_role(user.id, Roles.ADMIN)
			user.roles.append(Roles.ADMIN)
			rc.users.confirm(user.id)
			flash(u'Администратор успешно добавлен', 'success')
			return redirect(url_for('.users_info', id=user.id))
		flash(u'Произошла ошибка при регистрации администратора.', 'error')
	return dict(form=form)


@bp.route('/users/<int:id>/', methods=['GET', 'POST'])
@template('admin/users/info/info.html')
@context(user_context_provider)
@permission_required_on_advertiser('view_advertiser')
@permission_required_on_advertiser('do_advertiser_block', post=True)
@permission_required_on_affiliate('view_affiliate')
@permission_required_on_affiliate('do_affiliate_block', post=True)
def users_info(id, user):
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
	return dict(form=form)


@bp.route('/users/<int:id>/login/')
@context(user_context_provider)
@permission_required_on_advertiser('do_advertiser_login')
@permission_required_on_affiliate('do_affiliate_login')
def users_info_login(id, user):
	session['user_id'] = user.id
	session.permanent = False
	return redirect(url_for('site.gateway'))


@bp.route('/users/<int:id>/offers/')
@template('admin/users/info/offers.html')
@context(user_context_provider)
@permission_required_on_advertiser('view_advertiser_offers')
@permission_required_on_affiliate('view_affiliate_offers')
@paginated(OFFERS_PER_PAGE)
def users_info_offers(id, user, **kwargs):
	if user.is_advertiser:
		offers, count = rc.offers.list(advertiser_id=user.id, **kwargs)
	else:
		offers, count = rc.offers.list_requested(user.id, **kwargs)
	return dict(offers=offers, count=count)


@bp.route('/users/<int:id>/edit/', methods=['GET', 'POST'])
@template('admin/users/info/edit.html')
@context(user_context_provider)
@permission_required_on_advertiser('do_advertiser_edit')
@permission_required_on_affiliate('do_affiliate_edit')
def users_info_edit(id, user):
	FormClass = forms.AdminAdminEditForm if user.is_admin \
		else forms.AdminAdvertiserEditForm if user.is_advertiser \
		else forms.AdminAffiliateEditForm
	form = FormClass(request.form, obj=user)	
	if request.method == 'POST' and form.validate():
		form.populate_obj(user)
		if user.updated():
			rc.users.update(user)
			flash(u'Профиль пользователя успешно изменен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.users_info', id=user.id))
	return dict(form=form)


@bp.route('/users/<int:id>/password/', methods=['GET', 'POST'])
@template('admin/users/info/password.html')
@context(user_context_provider)
@permission_required_on_advertiser('do_advertiser_edit')
@permission_required_on_affiliate('do_affiliate_edit')
def users_info_password_change(id, user):
	form = forms.AdminPasswordChangeForm(request.form)
	if request.method == 'POST' and form.validate():
		form.populate_obj(user)
		rc.users.update(user)
		flash(u'Пароль пользователя успешно изменен', 'success')
		return redirect(url_for('.users_info', id=user.id))
	return dict(form=form)


@bp.route('/users/<int:id>/a/lists/add/')
@context(user_context_provider)
@permission_required_on_advertiser('do_advertiser_edit')
@permission_required_on_affiliate('do_affiliate_edit')
def users_info_lists_add(id, user):
	if mmail.lists_add_user(user, mail_if_failed=False):
		flash(u'Пользователь добавлен в списки рассылки', 'success')
	else:
		flash(u'Ошибка при добавлении пользователя в списки рассылки', 'error')
	return redirect(url_for('.users_info', id=user.id))


@bp.route('/users/<int:id>/balance/', methods=['GET', 'POST'])
@template('admin/users/info/balance.html')
@context(user_context_provider)
@permission_required_on_advertiser('view_advertiser_finances')
@permission_required_on_advertiser('do_advertiser_balance_add', post=True)
@permission_required_on_affiliate('view_affiliate_finances')
@paginated(ACCOUNTING_ENTRIES_PER_PAGE)
def users_info_balance(id, user, **kwargs):
	form = forms.BalanceForm(request.form)
	entries, count = rc.accounts.entries_list(user.account.id, **kwargs)
	if user.is_advertiser and request.method == 'POST' and form.validate():
		rc.users.add_to_advertiser_account(user.id, round(form.amount.data, 2))
		flash(u'Баланс успешно пополнен', 'success')
		return redirect(request.url)
	return dict(entries=entries, count=count, form=form)


@bp.route('/users/<int:id>/finances/')
@template('admin/users/info/finances.html')
@context(user_context_provider)
@permission_required_on_advertiser('view_advertiser_finances')
@permission_required_on_affiliate('view_affiliate_finances')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def users_info_finances(id, user, **kwargs):
	form = forms.DebtFilterForm(request.args)
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debts(aff_id=user.id, **kwargs)
		overall_debt = rc.withdrawals.overall_debt(aff_id=user.id, **kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(debts=debts, count=count, overall_debt=overall_debt, form=form)


@bp.route('/users/<int:id>/groups/', methods=['GET', 'POST'])
@template('admin/users/info/groups.html')
@context(user_context_provider)
@superadmin_required()
def users_info_groups(id, user):
	permissions = AdminPermissions.query.get_or_create(user_id=user.id)
	form = forms.AdminGroupsForm(request.form, obj=permissions)
	if request.method == 'POST' and form.validate():
		form.populate_obj(permissions)
		permissions.save()
		flash(u'Группы успешно обновлены', 'success')
		return redirect(request.url)
	return dict(form=form)


@bp.route('/users/<int:id>/stats/offer/')
@template('admin/users/info/stats/offer.html')
@context(user_context_provider)
@permission_required_on_advertiser('view_advertiser_stats')
@permission_required_on_affiliate('view_affiliate_stats')
@sorted('clicks_count', 'desc')
@paginated(OFFER_STATS_PER_PAGE)
def users_info_stats_offer(id, user, **kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_user(user, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)


@bp.route('/users/<int:id>/stats/subid/')
@template('admin/users/info/stats/sub-id.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('clicks_count', 'desc')
@paginated(SUB_ID_STATS_PER_PAGE)
def users_info_stats_sub_id(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_sub_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)


@bp.route('/users/<int:id>/stats/sourceid/')
@template('admin/users/info/stats/source-id.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('clicks_count', 'desc')
@paginated(SOURCE_ID_STATS_PER_PAGE)
def users_info_stats_source_id(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_source_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)


@bp.route('/users/<int:id>/stats/referer/')
@template('admin/users/info/stats/referer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('clicks_count', 'desc')
@paginated(REFERER_STATS_PER_PAGE)
def users_info_stats_referer(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_referer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)


@bp.route('/users/<int:id>/stats/keywords/')
@template('admin/users/info/stats/keywords.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('clicks_count', 'desc')
@paginated(KEYWORDS_STATS_PER_PAGE)
def users_info_stats_keywords(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)


@bp.route('/users/<int:id>/stats/suboffer/')
@template('admin/users/info/stats/suboffer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)


@bp.route('/users/<int:id>/stats/suboffer/sub_id/')
@template('admin/users/info/stats/suboffer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_sub_id(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	kwargs.update(form.sub_ids_from_string(request.args.get('sub_ids')))
	stats, count = rc.offer_stats.list_suboffer_by_sub_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)


@bp.route('/users/<int:id>/stats/suboffer/source_id/')
@template('admin/users/info/stats/suboffer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_source_id(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(source_id=request.args.get('source_id'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_source_id(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)


@bp.route('/users/<int:id>/stats/suboffer/referer/')
@template('admin/users/info/stats/suboffer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_referer(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(referer=request.args.get('referer'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_referer(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)


@bp.route('/users/<int:id>/stats/suboffer/keywords/')
@template('admin/users/info/stats/suboffer.html')
@context(user_context_provider)
@permission_required('view_affiliate_stats')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def users_info_stats_suboffer_keywords(id, user, **kwargs):
	offers, _ = rc.offers.list_requested(user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(keywords=request.args.get('keywords'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_keywords(aff_id=user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)
