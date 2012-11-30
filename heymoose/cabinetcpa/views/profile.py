# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash
from heymoose import app, signals, resource
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only
from heymoose.forms import forms
from heymoose.utils import robokassa
from heymoose.views.decorators import template, paginated


ACCOUNTING_ENTRIES_PER_PAGE = app.config.get('ACCOUNTING_ENTRIES_PER_PAGE', 20)


@bp.route('/profile')
@template('cabinetcpa/profile/info.html')
def profile():
	referral_offer = resource.offers.get_referral_offer()
	return dict(referral_offer=referral_offer)

@bp.route('/profile/sendmail')
def profile_sendmail():
	signals.confirmation_email_requested.send(app, user=g.user)
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

@bp.route('/profile/balance', methods=['GET', 'POST'])
@advertiser_only
@template('cabinetcpa/profile/balance.html')
@paginated(ACCOUNTING_ENTRIES_PER_PAGE)
def profile_balance(**kwargs):
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		url = robokassa.account_pay_url(
			account_id=g.user.advertiser_account.id,
			sum=round(form.amount.data, 2),
			email=g.user.email)
		return redirect(url)
	entries, count = resource.accounts.entries_list(g.user.account.id, **kwargs)
	return dict(entries=entries, count=count, form=form)

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