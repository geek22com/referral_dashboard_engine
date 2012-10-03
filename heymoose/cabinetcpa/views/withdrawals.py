# -*- coding: utf-8 -*-
from flask import g, flash, redirect, request, url_for
from heymoose import app, resource as rc
from heymoose.utils.convert import to_unixtime
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only
from heymoose.views.decorators import template, sorted, paginated
from datetime import datetime


DEBTS_PER_PAGE = app.config.get('DEBTS_PER_PAGE', 20)


@bp.route('/withdrawals/')
@affiliate_only
def withdrawals():
	return redirect(url_for('.withdrawals_order'))


@bp.route('/withdrawals/order/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/withdrawals/order.html')
@sorted('pending', 'desc')
@paginated(DEBTS_PER_PAGE)
def withdrawals_order(**kwargs):
	if request.method == 'POST':
		rc.withdrawals.order_withdrawal(g.user.id)
		flash(u'Выплата успешно заказана', 'success')
		return redirect(request.url)
	kwargs.update({'from' : 0, 'to' : to_unixtime(datetime.now(), True)})
	debts, count = rc.withdrawals.list_debts(aff_id=g.user.id, **kwargs)
	overall_debt = rc.withdrawals.overall_debt(aff_id=g.user.id, **kwargs)
	return dict(debts=debts, count=count, overall_debt=overall_debt)


@bp.route('/withdrawals/history/')
@affiliate_only
@template('cabinetcpa/withdrawals/history.html')
@paginated(DEBTS_PER_PAGE)
def withdrawals_history(**kwargs):
	debts, count = rc.withdrawals.list_ordered_by_affiliate(aff_id=g.user.id, **kwargs)
	return dict(debts=debts, count=count)
