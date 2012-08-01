# -*- coding: utf-8 -*-
from flask import request
from heymoose import resource as rc
from heymoose.admin import blueprint as bp
from heymoose.views.decorators import template, paginated
from heymoose.utils.config import config_accessor
from heymoose.forms import forms

API_ERRORS_PER_PAGE = config_accessor('API_ERRORS_PER_PAGE', 20)

@bp.route('/logs/errors')
@template('admin/logs/api.html')
@paginated(API_ERRORS_PER_PAGE)
def logs_api(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	errors, count = rc.errors.list(**kwargs) if form.validate() else ([], 0)
	return dict(errors=errors, count=count, form=form)