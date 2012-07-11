# -*- coding: utf-8 -*-
from flask import g, flash, redirect, url_for
from heymoose import resource as rc
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only
from heymoose.views.decorators import template


@bp.route('/withdrawals')
@affiliate_only
@template('cabinetcpa/withdrawals.html')
def withdrawals():
	withdrawals = rc.accounts.withdrawals_list_by_affiliate(g.user.id)
	return dict(withdrawals=withdrawals)

@bp.route('/withdrawals/create/', methods=['POST'])
@affiliate_only
def withdrawals_create():
	rc.accounts.create_withdrawal(g.user.account.id)
	flash(u'Выплата успешно заказана', 'success')
	return redirect(url_for('.withdrawals'))