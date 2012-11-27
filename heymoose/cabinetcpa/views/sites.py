# -*- coding: utf-8 -*-
from flask import g, request, redirect, url_for, flash
from heymoose import app, resource as rc
from heymoose.data.models import Site
from heymoose.forms import forms
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only
from heymoose.views.decorators import template, context, sorted, paginated


SITES_PER_PAGE = app.config.get('SITES_PER_PAGE', 20)

site_context = context(lambda id, **kwargs: dict(site=rc.sites.get_by_id(id)))


@bp.route('/sites/')
@affiliate_only
@template('cabinetcpa/sites/list.html')
@sorted('creation_time', 'desc')
@paginated(SITES_PER_PAGE)
def sites_list(**kwargs):
	sites, count = rc.sites.list(aff_id=g.user.id, **kwargs)
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
		flash(u'Площадка успешно добавлена. Она станет акивной после проверки администрацией.', 'success')
		return redirect(url_for('.sites_list'))
	return dict(form=form)


@bp.route('/sites/<int:id>/')
@affiliate_only
@template('cabinetcpa/sites/info/info.html')
@site_context
def sites_info(id, site):
	return dict()


@bp.route('/sites/<int:id>/edit/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/sites/info/edit.html')
@site_context
def sites_info_edit(id, site):
	form = forms.site_form_by_type(site.type, request.form, obj=site)
	if request.method == 'POST' and form.validate():
		form.populate_obj(site)
		rc.sites.update(site)
		flash(u'Площадка успешно изменена', 'success')
		return redirect(url_for('.sites_info', id=site.id))
	return dict(form=form)
