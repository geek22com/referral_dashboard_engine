# -*- coding: utf-8 -*-
from flask import g, redirect, url_for, abort
from heymoose import app
from heymoose.cabinetcpa import blueprint as bp


@bp.route('/')
def index():
	if g.user.is_affiliate:
		return redirect(url_for('.sites_list'))
	elif g.user.is_advertiser:
		return redirect(url_for('.offers_list'))
	else:
		app.logger.error("Shit happened: user has unknown role in user cabinet")
		abort(403)



