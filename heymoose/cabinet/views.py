# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash
from heymoose import app
from heymoose.cabinet import blueprint as bp
from heymoose.forms import forms
from heymoose.core.data import OrderTypes
from heymoose.utils.shortcuts import do_or_abort
import heymoose.core.actions as actions
import base64


@bp.route('/')
def index():
	if g.user.is_admin():
		return redirect(url_for('admin.index'))
	elif g.user.is_developer():
		return redirect(url_for('.apps'))
	elif g.user.is_customer():
		return redirect(url_for('.orders'))
	else:
		app.logger().error("Shit happened: user has unknown role in user cabinet")
		abort(403)


@bp.route('/orders/')
def orders():
	return render_template('cabinet/orders.html', orders=g.user.orders)

@bp.route('/orders/new', methods=['GET', 'POST'])
def orders_new():
	if request.method == 'POST':
		ordertype = request.form['ordertype']
		if ordertype == OrderTypes.REGULAR:
			rform = forms.RegularOrderForm(request.form)
			bform = forms.BannerOrderForm()
			vform = forms.VideoOrderForm()
			
			if rform.validate():
				form = rform
				do_or_abort(actions.orders.add_regular_order,
					user_id=g.user.id,
					title=form.ordername.data,
					url=form.orderurl.data,
					balance=form.orderbalance.data,
					cpa=form.ordercpa.data,
					description=form.orderdesc.data,
					image=base64.encodestring(request.files['orderimage'].stream.read()),
					auto_approve=form.orderautoapprove.data,
					allow_negative_balance=form.orderallownegativebalance.data,
					male=form.ordermale.data,
					min_age=form.orderminage.data,
					max_age=form.ordermaxage.data)
				flash(u'Заказ успешно создан.', 'success')
				return redirect(url_for('.orders'))
				
				
		elif ordertype == OrderTypes.BANNER:
			rform = forms.RegularOrderForm()
			bform = forms.BannerOrderForm(request.form)
			vform = forms.VideoOrderForm()
			
			if bform.validate():
				form = bform
				do_or_abort(actions.orders.add_banner_order,
					user_id=g.user.id,
					title=form.ordername.data,
					url=form.orderurl.data,
					balance=form.orderbalance.data,
					cpa=form.ordercpa.data,
					image=base64.encodestring(request.files['orderimage'].stream.read()),
					auto_approve=form.orderautoapprove.data,
					allow_negative_balance=form.orderallownegativebalance.data,
					male=form.ordermale.data,
					min_age=form.orderminage.data,
					max_age=form.ordermaxage.data)
				flash(u'Заказ успешно создан.', 'success')
				return redirect(url_for('.orders'))
			
		elif ordertype == OrderTypes.VIDEO:
			rform = forms.RegularOrderForm()
			bform = forms.BannerOrderForm()
			vform = forms.VideoOrderForm(request.form)
			
			if vform.validate():
				form = vform
				do_or_abort(actions.orders.add_video_order,
					user_id=g.user.id,
					title=form.ordername.data,
					url=form.orderurl.data,
					balance=form.orderbalance.data,
					cpa=form.ordercpa.data,
					video_url=form.ordervideourl.data,
					auto_approve=form.orderautoapprove.data,
					allow_negative_balance=form.orderallownegativebalance.data,
					male=form.ordermale.data,
					min_age=form.orderminage.data,
					max_age=form.ordermaxage.data)
				flash(u'Заказ успешно создан.', 'success')
				return redirect(url_for('.orders'))
	else:
		ordertype = 'REGULAR'
		rform = forms.RegularOrderForm()
		bform = forms.BannerOrderForm()
		vform = forms.VideoOrderForm()
			
	return render_template('cabinet/orders-new.html', 
		rform=rform, bform=bform, vform=vform, ordertype=ordertype.lower())


@bp.route('/apps/')
def apps():
	return render_template('cabinet/apps.html', apps=g.user.apps)

@bp.route('/apps/new', methods=['GET', 'POST'])
def apps_new():
	form = forms.AppForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.apps.add_app,
			user_id=g.user.id,
			callback=form.appcallback.data,
			url=form.appurl.data,
			platform=form.appplatform.data)
		flash(u'Приложение успешно добавлено', 'success')
		return redirect(url_for('.apps'))
	return render_template('cabinet/apps-new.html', form=form)


@bp.route('/info')
def info():
	return render_template('cabinet/info.html')

@bp.route('/info/balance/pay', methods=['GET', 'POST'])
def balance_pay():
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.users.increase_customer_balance,
				g.user.id, int(form.amount.data))
		flash(u'Баланс успешно пополнен', 'success')
		return redirect(url_for('.info'))
	return render_template('cabinet/info-balance-pay.html', form=form) 
	

@bp.route('/roles/new/customer')
def become_customer():
	if not g.user.is_customer():
		do_or_abort(actions.users.become_customer, g.user.id)
		flash(u'Поздравляем, теперь вы рекламодатель!', 'success')
	else:
		flash(u'Вы уже являетесь рекламодателем', 'error')
	return redirect(url_for('.orders'))

@bp.route('/roles/new/developer')
def become_developer():
	if not g.user.is_developer():
		do_or_abort(actions.users.become_developer, g.user.id)
		flash(u'Поздравляем, теперь вы разработчик!', 'success')
	else:
		flash(u'Вы уже являетесь разработчиком', 'error')
	return redirect(url_for('.apps'))





