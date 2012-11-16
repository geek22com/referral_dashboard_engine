# -*- coding: utf-8 -*-
from flask import g, redirect, url_for
from heymoose import app, resource as rc
from heymoose.views import excel
from heymoose.views.decorators import template, paginated
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only


CASHBACKS_PER_PAGE = app.config.get('CASHBACKS_PER_PAGE', 20)
CASHBACK_INVITES_PER_PAGE = app.config.get('CASHBACK_INVITES_PER_PAGE', 20)


@bp.route('cabinetcpa/cashback/')
@affiliate_only
def cashback():
	return redirect(url_for('.cashback_list'))


@bp.route('cabinetcpa/cashback/list/')
@affiliate_only
@template('cabinetcpa/cashback/list.html')
@paginated(CASHBACKS_PER_PAGE)
def cashback_list(**kwargs):
	cashbacks, count = rc.cashbacks.list(g.user.id, **kwargs)
	return dict(cashbacks=cashbacks, count=count)


@bp.route('cabinetcpa/cashback/invites/')
@affiliate_only
@template('cabinetcpa/cashback/invites.html')
@paginated(CASHBACK_INVITES_PER_PAGE)
def cashback_invites(**kwargs):
	invites, count = rc.cashbacks.list_invites(g.user.id, **kwargs)
	return dict(invites=invites, count=count)
