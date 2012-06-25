# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash
from heymoose import app, resource
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only, affiliate_only
from heymoose.forms import forms
from heymoose.utils import robokassa
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.mail import transactional as mail


@bp.route('/profile')
def profile():
	return render_template('cabinetcpa/profile/info.html')

@bp.route('/profile/sendmail', methods=['POST'])
def profile_sendmail():
	mail.user_confirm_email(g.user)
	flash(u'Письмо выслано повторно', 'success')
	return redirect(url_for('.profile'))

@bp.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
	FormClass = forms.AdvertiserEditForm if g.user.is_advertiser else forms.AffiliateEditForm
	form = FormClass(request.form, obj=g.user)
	if request.method == 'POST' and form.validate():
		form.populate_obj(g.user)
		if g.user.updated():
			resource.users.update(g.user)
			flash(u'Профиль успешно изменен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.profile'))
	return render_template('cabinetcpa/profile/edit.html', form=form)

@bp.route('/profile/edit/password', methods=['GET', 'POST'])
def profile_password_change():
	form = forms.PasswordChangeForm(request.form, user=g.user)
	if request.method == 'POST' and form.validate():
		form.populate_obj(g.user)
		resource.users.update(g.user)
		flash(u'Пароль успешно изменен', 'success')
		return redirect(url_for('.profile'))
	return render_template('cabinetcpa/profile/password-change.html', form=form)

@bp.route('/profile/withdrawals')
@affiliate_only
def profile_withdrawals():
	withdrawals = resource.accounts.withdrawals_list(g.user.account.id)
	withdrawals = [w for w in withdrawals if w.done]
	return render_template('cabinetcpa/profile/withdrawals.html', withdrawals=withdrawals)

@bp.route('/profile/balance', methods=['GET', 'POST'])
@advertiser_only
def profile_balance():
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		url = robokassa.account_pay_url(
			account_id=g.user.customer_account.id,
			sum=round(form.amount.data, 2),
			email=g.user.email)
		return redirect(url)
	page = current_page()
	per_page = app.config.get('ACCOUNTING_ENTRIES_PER_PAGE', 20)
	offset, limit = page_limits(page, per_page)
	entries, count = resource.accounts.entries_list(g.user.account.id, offset=offset, limit=limit)
	pages = paginate(page, count, per_page)
	return render_template('cabinetcpa/profile/balance.html', entries=entries, pages=pages, form=form)

@bp.route('/profile/balance/success', methods=['POST'])
@advertiser_only
def info_balance_success():
	sum = request.form.get('OutSum', None) or abort(400)
	return render_template('cabinetcpa/profile/balance-success.html', sum=float(sum))

@bp.route('/profile/balance/fail', methods=['POST'])
@advertiser_only
def info_balance_fail():
	sum = request.form.get('OutSum', None) or abort(400)
	return render_template('cabinetcpa/profile/balance-fail.html', sum=float(sum))