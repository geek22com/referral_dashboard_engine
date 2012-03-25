# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash, jsonify
from heymoose import app
from heymoose.cabinet import blueprint as bp
from heymoose.forms import forms
from heymoose.core import actions
from heymoose.utils import convert
from heymoose.utils.shortcuts import do_or_abort, paginate
from heymoose.views.common import json_get_ctr
from heymoose.cabinet.decorators import developer_only


@bp.route('/apps/')
@developer_only
def apps():
	page = convert.to_int(request.args.get('page'), 1)
	count = actions.apps.get_apps_count(user_id=g.user.id)
	per_page = app.config.get('ADMIN_APPS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	aps = do_or_abort(actions.apps.get_apps, user_id=g.user.id,
					offset=offset, limit=limit, full=True)
	return render_template('cabinet/apps.html', apps=aps, pages=pages)

@bp.route('/apps/new', methods=['GET', 'POST'])
@developer_only
def apps_new():
	form = forms.AppForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.apps.add_app,
			title=form.apptitle.data,
			user_id=g.user.id,
			callback=form.appurl.data,
			url=form.appurl.data,
			platform=form.appplatform.data)
		flash(u'Приложение успешно добавлено', 'success')
		return redirect(url_for('.apps'))
	return render_template('cabinet/apps-new.html', form=form)

@bp.route('/apps/<int:id>/')
@developer_only
def apps_info(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return render_template('cabinet/apps-info.html', app=app)

@bp.route('/apps/<int:id>/stats')
@developer_only
def apps_info_stats(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return render_template('cabinet/apps-info-stats.html', app=app)


@bp.route('/apps/q/ctr')
@developer_only
def ajax_apps_ctr():
	'''ids = request.args.getlist('id', int)
	stats = actions.stats.get_stats_ctr_by_ids(app_ids=ids, fm=times.delta(datetime.now(), days=-3))
	result = dict([(s.id, dict(actions=s.actions, shows=s.shows, ctr='%.4f' % s.ctr)) for s in stats])
	return jsonify(result)'''
	return jsonify(disabled=1)

@bp.route('/apps/<int:id>/stats/q/ctr/')
@developer_only
def ajax_apps_info_stats_ctr(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return json_get_ctr(app_id=app.id)