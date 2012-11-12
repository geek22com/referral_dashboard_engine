# -*- coding: utf-8 -*-
from flask import request, redirect, url_for
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import permission_required
from heymoose.views.decorators import template, sorted, paginated


USERS_PER_PAGE = app.config.get('USERS_PER_PAGE', 20)


@bp.route('/fraud/')
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


@bp.route('/fraud/sites/blacklist/')
@permission_required('view_fraud')
def fraud_sites_blacklist():
	return 'OK'