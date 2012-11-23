# -*- coding: utf-8 -*-
from flask import g, request, redirect, url_for, flash
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.admin import blueprint as bp
from heymoose.views.decorators import template, context, sorted, paginated


SITES_PER_PAGE = app.config.get('SITES_PER_PAGE', 20)

site_context = context(lambda id, **kwargs: dict(site=rc.sites.get_by_id(id)))


@bp.route('/sites/')
@template('admin/sites/list.html')
@sorted('last_change_time', 'desc')
@paginated(SITES_PER_PAGE)
def sites_list(**kwargs):
	sites, count = rc.sites.list(**kwargs)
	return dict(sites=sites, count=count)


@bp.route('/sites/<int:id>/')
@template('admin/sites/info/info.html')
@site_context
def sites_info(id, site):
	return dict()


@bp.route('/sites/<int:id>/moderation/', methods=['GET', 'POST'])
@template('admin/sites/info/moderation.html')
@site_context
def sites_info_moderation(id, site):
	form = forms.ModerationForm(request.form, obj=site)
	if request.method == 'POST' and form.validate():
		form.populate_obj(site)
		rc.sites.moderate(site)
		flash(u'Площадка успешно изменена', 'success')
		return redirect(url_for('.sites_info', id=site.id))
	return dict(form=form)
