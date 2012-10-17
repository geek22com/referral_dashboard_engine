from flask import request, redirect, url_for, send_file
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.data.enums import DebtDateKinds
from heymoose.views import excel
from heymoose.views.decorators import template, sorted, paginated
from heymoose.admin import blueprint as bp
from heymoose.admin.helpers import superadmin_required


FINANCES_PER_PAGE = app.config.get('FINANCES_PER_PAGE', 20)


@bp.route('/finances/')
@superadmin_required()
def finances():
	return redirect(url_for('.finances_withdrawals_affiliate'))


@bp.route('/finances/withdrawals/affiliate/')
@superadmin_required()
@template('admin/finances/withdrawals-affiliate.html')
@paginated(FINANCES_PER_PAGE)
def finances_withdrawals_affiliate(**kwargs):
	debts, count = rc.withdrawals.list_ordered_by_affiliate(**kwargs)
	overall_debt = rc.withdrawals.sum_ordered()
	return dict(debts=debts, count=count, overall_debt=overall_debt)


@bp.route('/finances/withdrawals/offer/')
@superadmin_required()
@template('admin/finances/withdrawals-offer.html')
@paginated(FINANCES_PER_PAGE)
def finances_withdrawals_offer(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	debts, count = rc.withdrawals.list_ordered_by_offer(**kwargs) if form.validate() else ([], 0)
	return dict(debts=debts, count=count, form=form)


@bp.route('/finances/debts/')
@superadmin_required()
@template('admin/finances/debts.html')
@sorted('pending', 'desc')
@paginated(FINANCES_PER_PAGE)
def finances_debts(**kwargs):
	form = forms.DebtFilterForm(request.args)
	if request.args.get('format') == 'xls' and form.validate():
		debts, _ = rc.withdrawals.list_debts(offset=0, limit=999999, ordering='PENDING', direction='DESC',
			**form.backend_args())
		return send_file(excel.debts_to_xls(debts), as_attachment=True, attachment_filename='debts.xls')
	if form.validate():
		kwargs.update(form.backend_args())
		debts, count = rc.withdrawals.list_debts(**kwargs)
		overall_debt = rc.withdrawals.overall_debt(**kwargs)
	else:
		debts, count, overall_debt = [], 0, None
	return dict(debts=debts, count=count, overall_debt=overall_debt, form=form)


@bp.route('/finances/payments/')
@superadmin_required()
@template('admin/finances/payments.html')
@paginated(FINANCES_PER_PAGE)
def finances_payments(**kwargs):
	form = forms.PaymentFilterForm(request.args)
	kwargs.update(form.backend_args())
	payments, count = rc.withdrawals.list_payments(**kwargs) if form.validate() else ([], 0)
	return dict(payments=payments, count=count, form=form)


@bp.route('/finances/payments/payments.xml')
@superadmin_required()
def finances_payments_xml():
	form = forms.PaymentFilterForm(request.args)
	xml = rc.withdrawals.list_payments_xml(**form.backend_args())
	return app.response_class(xml, mimetype='application/xml')
