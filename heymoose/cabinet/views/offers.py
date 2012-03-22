# -*- coding: utf-8 -*-
from flask import render_template, request, flash
from heymoose.forms import forms
from heymoose.cabinet import blueprint as bp
from heymoose.cabinet.decorators import advertiser_only, partner_only

offer = dict(id=1)

@bp.route('/offers/')
def offers_list():
	return render_template('cabinet/offers/list.html')

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
	return render_template('cabinet/offers/new.html', form=form, tmpl=tmpl)

@bp.route('/offers/<int:id>')
def offers_info(id):
	return render_template('cabinet/offers/info/info.html', offer=offer)

@bp.route('/offers/<int:id>/edit')
@advertiser_only
def offers_info_edit(id):
	return render_template('cabinet/offers/info/edit.html', offer=offer)

@bp.route('/offers/<int:id>/actions')
def offers_info_actions(id):
	form = forms.SubOfferForm()
	return render_template('cabinet/offers/info/actions.html', offer=offer, form=form)

@bp.route('/offers/<int:id>/materials')
def offers_info_materials(id):
	return render_template('cabinet/offers/info/materials.html', offer=offer)

@bp.route('/offers/<int:id>/partners')
@advertiser_only
def offers_info_partners(id):
	return render_template('cabinet/offers/info/partners.html', offer=offer)

@bp.route('/offers/<int:id>/balance')
@advertiser_only
def offers_info_balance(id):
	return render_template('cabinet/offers/info/balance.html', offer=offer)

@bp.route('/offers/<int:id>/stats')
def offers_info_stats(id):
	return render_template('cabinet/offers/info/stats.html', offer=offer)
