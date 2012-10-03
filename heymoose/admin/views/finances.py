from flask import request, redirect, url_for
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.enums import DebtDateKinds
from heymoose.views.decorators import template, sorted, paginated
from heymoose.admin import blueprint as bp


DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)


@bp.route('/finances/')
def finances():
	return redirect(url_for('.finances_withdrawals_affiliate'))


@bp.route('/finances/withdrawals/affiliate/')
@template('admin/finances/withdrawals-affiliate.html')
@paginated(DEBTS_PER_PAGE)
def finances_withdrawals_affiliate(**kwargs):
	debts, count = rc.withdrawals.list_ordered_by_affiliate(**kwargs)
	overall_debt = rc.withdrawals.sum_ordered()
	return dict(debts=debts, count=count, overall_debt=overall_debt)


@bp.route('/finances/withdrawals/offer/')
@template('admin/finances/withdrawals-offer.html')
@paginated(DEBTS_PER_PAGE)
def finances_withdrawals_offer(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	debts, count = rc.withdrawals.list_ordered_by_offer(**kwargs) if form.validate() else ([], 0)
	return dict(debts=debts, count=count, form=form)


@bp.route('/finances/debts/')
@template('admin/finances/debts.html')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def finances_debts(**kwargs):
	form = forms.DebtFilterForm(request.args)
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debts(**kwargs)
		overall_debt = rc.withdrawals.overall_debt(**kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(debts=debts, count=count, overall_debt=overall_debt, form=form)
