# -*- coding: utf-8 -*-
from flask import g, request, redirect, url_for, flash
from heymoose import app, signals, resource as rc
from heymoose.forms import forms
from heymoose.data.mongo import actions as mongo
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


@bp.route('/sites/<int:id>/', methods=['GET', 'POST'])
@template('admin/sites/info/info.html')
@site_context
def sites_info(id, site):
	form = forms.SiteCommentForm(request.form)
	if request.method == 'POST' and form.validate():
		mongo.site_comments_post(site, form.text.data, admin=True)
		signals.site_commented_by_admin.send(app, site=site, comment=form.text.data)
		flash(u'Комментарий успешно добавлен', 'success')
		return redirect(request.url)
	comments = mongo.site_comments_list(site)
	moderation_form = forms.ModerationForm(obj=site)
	return dict(form=form, comments=comments, moderation_form=moderation_form)


@bp.route('/sites/<int:id>/moderation/', methods=['POST'])
@site_context
def sites_info_moderation(id, site):
	form = forms.ModerationForm(request.form, obj=site)
	if form.validate():
		form.populate_obj(site)
		site.admin_comment = None
		rc.sites.moderate(site)
		if site.updated():
			signals.site_moderated.send(app, site=site)
		flash(u'Площадка успешно изменена', 'success')
	else:
		flash(u'Ошибка при модерации площадки', 'danger')
	return redirect(url_for('.sites_info', id=site.id))