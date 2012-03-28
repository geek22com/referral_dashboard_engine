# -*- coding: utf-8 -*-
from flask import render_template, request, flash
from heymoose.forms import forms
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only

site = dict(id=1)

@bp.route('/sites/')
@affiliate_only
def sites_list():
	return render_template('cabinetcpa/sites/list.html')

@bp.route('/sites/new')
@affiliate_only
def sites_new():
	form = forms.SiteForm()
	if request.method == 'POST' and form.validate():
		flash(u'Все ОК', 'success')
	return render_template('cabinetcpa/sites/new.html', form=form)

@bp.route('/sites/<int:id>')
@affiliate_only
def sites_info(id):
	return render_template('cabinetcpa/sites/info/info.html', site=site)

@bp.route('/sites/<int:id>/edit')
@affiliate_only
def sites_info_edit(id):
	return render_template('cabinetcpa/sites/info/edit.html', site=site)

@bp.route('/sites/<int:id>/stats')
@affiliate_only
def sites_info_stats(id):
	return render_template('cabinetcpa/sites/info/stats.html', site=site)