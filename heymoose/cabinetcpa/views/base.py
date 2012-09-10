# -*- coding: utf-8 -*-
from flask import g, abort
from heymoose.cabinetcpa import blueprint as bp
from heymoose.views.decorators import template


@template('cabinetcpa/index-affiliate.html')
def index_affiliate():
	return dict()

@template('cabinetcpa/index-advertiser.html')
def index_advertiser():
	return dict()

@bp.route('/')
def index():
	if g.user.is_advertiser:
		return index_advertiser()
	elif g.user.is_affiliate:
		return index_affiliate()
	else:
		abort(403)
	
	



