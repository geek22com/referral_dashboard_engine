# -*- coding: utf-8 -*-
from flask import render_template, request
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.forms import forms


@bp.route('/stats/offer')
def stats_offer():
	form = forms.OfferStatsFilterForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_all(offset=offset, limit=limit,
			granted=form.requested.data, **form.range_args())
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('admin/stats/offer.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/affiliate')
def stats_affiliate():
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_affiliate(offset=offset, limit=limit, **form.range_args())
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('admin/stats/affiliate.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/advertiser')
def stats_advertiser():
	form = forms.AdvertiserStatsForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_advertiser(offset=offset, limit=limit, **form.backend_args())
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('admin/stats/advertiser.html', stats=stats, pages=pages, form=form)
