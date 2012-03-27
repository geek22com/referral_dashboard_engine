# -*- coding: utf-8 -*-
from flask import render_template, request, flash
from heymoose.forms import forms
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import advertiser_only

offer = dict(id=1)

@bp.route('/offers/')
def offers_list():
	return render_template('cabinetcpa/offers/list.html')

@bp.route('/offers/all')
def offers_all():
	return 'OK'

@bp.route('/offers/new')
@advertiser_only
def offers_new():
	tmpl = forms.SubOfferForm(prefix='suboffers-0-')
	form = forms.OfferForm(request.form)
	if request.method == 'POST' and form.validate():
		print form.suboffers.data
		flash(u'Все ОК', 'success')
	return render_template('cabinetcpa/offers/new.html', form=form, tmpl=tmpl)

@bp.route('/offers/<int:id>')
def offers_info(id):
	form = forms.OfferRequestForm()
	return render_template('cabinetcpa/offers/info/info.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/edit')
@advertiser_only
def offers_info_edit(id):
	return render_template('cabinetcpa/offers/info/edit.html', offer=offer)

@bp.route('/offers/<int:id>/actions')
def offers_info_actions(id):
	form = forms.SubOfferForm()
	return render_template('cabinetcpa/offers/info/actions.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/materials')
def offers_info_materials(id):
	return render_template('cabinetcpa/offers/info/materials.html', offer=offer)

@bp.route('/offers/<int:id>/requests')
@advertiser_only
def offers_info_requests(id):
	return render_template('cabinetcpa/offers/info/requests.html', offer=offer)

@bp.route('/offers/<int:id>/balance')
@advertiser_only
def offers_info_balance(id):
	return render_template('cabinetcpa/offers/info/balance.html', offer=offer)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	return render_template('cabinetcpa/offers/info/stats.html', offer=offer)

