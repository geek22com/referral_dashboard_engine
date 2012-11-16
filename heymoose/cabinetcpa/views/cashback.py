# -*- coding: utf-8 -*-
from flask import g, request, redirect, url_for, send_file
from heymoose import app, resource as rc
from heymoose.views import excel
from heymoose.views.decorators import template, paginated
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only


CASHBACKS_PER_PAGE = app.config.get('CASHBACKS_PER_PAGE', 20)
CASHBACK_INVITES_PER_PAGE = app.config.get('CASHBACK_INVITES_PER_PAGE', 20)
INFINITE_LIMIT = dict(offset=0, limit=999999)


@bp.route('/cashback/')
@affiliate_only
def cashback():
	return redirect(url_for('.cashback_list'))


@bp.route('/cashback/list/')
@affiliate_only
@template('cabinetcpa/cashback/list.html')
@paginated(CASHBACKS_PER_PAGE)
def cashback_list(**kwargs):
	if request.args.get('format') == 'xls':
		cashbacks, _ = rc.cashbacks.list(g.user.id, **INFINITE_LIMIT)
		return send_file(excel.cashbacks_to_xls(cashbacks), as_attachment=True, attachment_filename='cashback.xls')
	cashbacks, count = rc.cashbacks.list(g.user.id, **kwargs)
	return dict(cashbacks=cashbacks, count=count)


@bp.route('/cashback/invites/')
@affiliate_only
@template('cabinetcpa/cashback/invites.html')
@paginated(CASHBACK_INVITES_PER_PAGE)
def cashback_invites(**kwargs):
	if request.args.get('format') == 'xls':
		invites, _ = rc.cashbacks.list_invites(g.user.id, **INFINITE_LIMIT)
		return send_file(excel.cashback_invites_to_xls(invites), as_attachment=True, attachment_filename='cashback_invites.xls')
	invites, count = rc.cashbacks.list_invites(g.user.id, **kwargs)
	return dict(invites=invites, count=count)
