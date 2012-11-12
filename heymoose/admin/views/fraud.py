# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, flash
from heymoose import app, resource as rc
from heymoose.data.models import BlackListSite
from heymoose.forms import forms
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import permission_required
from heymoose.views.decorators import template, sorted, paginated


USERS_PER_PAGE = app.config.get('USERS_PER_PAGE', 20)
SITES_PER_PAGE = app.config.get('SITES_PER_PAGE', 20)


@bp.route('/fraud/')
@permission_required('view_fraud')
def fraud():
	return redirect(url_for('.fraud_users'))


@bp.route('/fraud/users/')
@permission_required('view_fraud')
@template('admin/fraud/users.html')
@sorted('rate', 'desc')
@paginated(USERS_PER_PAGE)
def fraud_users(**kwargs):
	form = forms.UserFilterForm(request.args)
	kwargs.update(form.backend_args())
	user_stats, count = rc.user_stats.list_fraud(**kwargs) if form.validate() else ([], 0)
	return dict(user_stats=user_stats, count=count, form=form)


@bp.route('/fraud/sites/blacklist/', methods=['GET', 'POST'])
@permission_required('view_fraud')
@template('admin/fraud/sites-blacklist.html')
@paginated(SITES_PER_PAGE)
def fraud_sites_blacklist(**kwargs):
	form = forms.BlackListSiteForm(request.form)
	if request.method == 'POST' and form.validate():
		if 'id' in request.form:
			site = rc.sites.blacklist_get(request.form.get('id'))
			form.populate_obj(site)
			if site.updated():
				rc.sites.blacklist_update(site)
				flash(u'Площадка успешно изменена.', 'success')
			else:
				flash(u'Вы не изменили ни одного поля.', 'warning')
		else:
			site = BlackListSite()
			form.populate_obj(site)
			rc.sites.blacklist_add(site)
			flash(u'Площадка занесена в черный список.', 'success')
		return redirect(request.url)
	sites, count = rc.sites.blacklist(**kwargs)
	for site in sites:
		site.form = forms.BlackListSiteForm(obj=site)
	return dict(sites=sites, count=count, form=form)


