# -*- coding: utf-8 -*-
from flask import g, request, redirect, url_for, flash
from heymoose import app, resource as rc
from heymoose.data.models import Site
from heymoose.forms import forms
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only
from heymoose.views.decorators import template, sorted, paginated


SITES_PER_PAGE = app.config.get('SITES_PER_PAGE', 20)


@bp.route('/sites/')
@affiliate_only
@template('cabinetcpa/sites/list.html')
@sorted('creation_time', 'desc')
@paginated(SITES_PER_PAGE)
def sites_list(**kwargs):
	sites, count = rc.sites.list(**kwargs)
	return dict(sites=sites, count=count)


@bp.route('/sites/new/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/sites/new.html')
def sites_new():
	site_type = request.args.get('type', '').upper()
	if not site_type: return dict()
	form = forms.site_form_by_type(site_type, request.form)
	if request.method == 'POST' and form.validate():
		site = Site(affiliate=g.user, type=site_type)
		form.populate_obj(site)
		rc.sites.add(site)
		flash(u'Площадка успешно добавлена', 'success')
		return redirect(url_for('.sites_list'))
	return dict(form=form)


@bp.route('/sites/<int:id>/')
@affiliate_only
def sites_info(id):
	return render_template('cabinetcpa/sites/info/info.html', site=site)


@bp.route('/sites/<int:id>/edit/')
@affiliate_only
def sites_info_edit(id):
	return render_template('cabinetcpa/sites/info/edit.html', site=site)
