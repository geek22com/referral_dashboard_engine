from flask import request
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.views.decorators import template, sorted, paginated
from heymoose.admin import blueprint as bp

DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)


@bp.route('/finances/')
@template('admin/finances.html')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def finances(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debts(**kwargs)
		overall_debt = rc.withdrawals.overall_debt(**kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(debts=debts, count=count, overall_debt=overall_debt, form=form)
