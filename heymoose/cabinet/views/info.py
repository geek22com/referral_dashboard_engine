# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash
from heymoose import app
from heymoose.cabinet import blueprint as bp
from heymoose.forms import forms
from heymoose.core import actions
from heymoose.utils import convert, robokassa
from heymoose.utils.shortcuts import paginate
from heymoose.utils.gen import generate_password_hash
from heymoose.mail import transactional as mail
from heymoose.cabinet.decorators import customer_only


@bp.route('/info', methods=['GET', 'POST'])
def info():
	if request.method == 'POST':
		mail.user_confirm_email(g.user)
		flash(u'Письмо выслано повторно', 'success')
	return render_template('cabinet/info.html')

@bp.route('/info/edit', methods=['GET', 'POST'])
def info_edit():
	form_args = dict(
		first_name = g.user.first_name,
		last_name = g.user.last_name,
		organization = g.user.organization,
		phone = g.user.phone,
		messenger_type = g.user.messenger_type,
		messenger_uid = g.user.messenger_uid
	)
	if g.user.is_customer():
		form = forms.CustomerEditForm(request.form, **form_args)
	else:
		form = forms.DeveloperEditForm(request.form, **form_args)
		
	if request.method == 'POST' and form.validate():
		upd_args = dict()
		if form.first_name.data != g.user.first_name: upd_args.update(first_name=form.first_name.data)
		if form.last_name.data != g.user.last_name: upd_args.update(last_name=form.last_name.data)
		if form.organization.data != g.user.organization: upd_args.update(organization=form.organization.data)
		if form.phone.data != g.user.phone: upd_args.update(phone=form.phone.data)
		
		messenger_type = form.messenger_type.data or None
		messenger_uid = form.messenger_uid.data or None
		if messenger_type != g.user.messenger_type or messenger_uid != g.user.messenger_uid:
			upd_args.update(messenger_type=messenger_type, messenger_uid=messenger_uid)
		if upd_args.keys():
			actions.users.update_user(g.user.id, **upd_args)
			flash(u'Профиль успешно изменен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.info'))
	
	return render_template('cabinet/info-edit.html', form=form)

@bp.route('/info/password', methods=['GET', 'POST'])
def info_password_change():
	form = forms.PasswordChangeForm(request.form, user=g.user)
	if request.method == 'POST' and form.validate():
		actions.users.update_user(g.user.id, password_hash=generate_password_hash(form.password.data))
		flash(u'Пароль успешно изменен', 'success')
		return redirect(url_for('.info'))
	return render_template('cabinet/info-password-change.html', form=form)

@bp.route('/info/balance', methods=['GET', 'POST'])
def info_balance():
	form = None
	if g.user.is_customer():
		form = forms.BalanceForm(request.form)
		if request.method == 'POST' and form.validate():
			sum = form.amount.data
			url = robokassa.account_pay_url(
				account_id=g.user.customer_account.id,
				sum=round(sum, 2),
				email=g.user.email)
			return redirect(url)
	
	account = g.user.customer_account if g.user.is_customer() else g.user.developer_account
	page = convert.to_int(request.args.get('page'), 1)
	count = actions.accounts.get_account_transactions_count(account.id)
	per_page = app.config.get('ADMIN_TRANSACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	transactions = actions.accounts.get_account_transactions(account_id=account.id, offset=offset, limit=limit)
	return render_template('cabinet/info-balance.html', transactions=transactions, pages=pages, form=form)
	
@bp.route('/info/balance/success', methods=['POST'])
@customer_only
def info_balance_success():
	sum = request.form.get('OutSum', None)
	if sum is None: abort(400)
	return render_template('cabinet/info-balance-success.html', sum=float(sum))

@bp.route('/info/balance/fail', methods=['POST'])
@customer_only
def info_balance_fail():
	sum = request.form.get('OutSum', None)
	if sum is None: abort(400)
	return render_template('cabinet/info-balance-fail.html', sum=float(sum))