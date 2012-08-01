# -*- coding: utf-8 -*-
from flask import request, flash, redirect, url_for
from heymoose import resource as rc
from heymoose.admin import blueprint as bp
from heymoose.views.decorators import template, paginated
from heymoose.utils.config import config_accessor

WITHDRAWALS_PER_PAGE = config_accessor('WITHDRAWALS_PER_PAGE', 20)


@bp.route('/operations/withdrawals/', methods=['GET', 'POST'])
@template('admin/operations/withdrawals.html')
@paginated(WITHDRAWALS_PER_PAGE)
def operations_withdrawals(**kwargs):
	ws = rc.accounts.withdrawals_list(**kwargs)
	return dict(withdrawals=ws.withdrawals, count=ws.count, ws=ws)

@bp.route('/operations/withdrawals/<int:id>/approve/', methods=['POST'])
def operations_withdrawals_approve(id):
	rc.accounts.approve_withdrawal(id)
	flash(u'Выплата успешно подтверждена', 'success')
	return redirect(url_for('.operations_withdrawals'))

@bp.route('/operations/approve', methods=['GET', 'POST'])
@template('admin/operations/approve.html')
def operations_approve():
	if request.method == 'POST':
		count = rc.actions.approve_expired()
		flash(u'{0} действий подтверждено'.format(count), 'success')
		return redirect(request.url)
	return dict()