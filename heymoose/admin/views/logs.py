# -*- coding: utf-8 -*-
from flask import render_template, request
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import superadmin_required
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.forms import forms


@bp.route('/logs/errors')
@superadmin_required()
def logs_api():
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('API_ERRORS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		errors, count = rc.errors.list(offset=offset, limit=limit, **form.range_args())
		pages = paginate(page, count, per_page)
	else:
		errors, pages = [], None
	return render_template('admin/logs/api.html', errors=errors, pages=pages, form=form)