# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect
from heymoose import resource as rc
from heymoose.admin import blueprint as bp


@bp.route('/operations/approve', methods=['GET', 'POST'])
def operations_approve():
	if request.method == 'POST':
		count = rc.actions.approve_expired()
		flash(u'{0} действий подтверждено'.format(count), 'success')
		return redirect(request.url)
	return render_template('admin/operations/approve.html')