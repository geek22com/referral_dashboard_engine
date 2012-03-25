# -*- coding: utf-8 -*-
from flask import g, redirect, url_for, abort
from heymoose import app
from heymoose.cabinet import blueprint as bp


@bp.route('/')
def index():
	if g.user.is_admin():
		return redirect(url_for('admin.index'))
	elif g.user.is_developer():
		return redirect(url_for('.apps'))
	elif g.user.is_customer():
		return redirect(url_for('.orders'))
	else:
		app.logger.error("Shit happened: user has unknown role in user cabinet")
		abort(403)



