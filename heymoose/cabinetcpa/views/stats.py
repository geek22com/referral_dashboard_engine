# -*- coding: utf-8 -*-
from flask import render_template, request, g
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only

@bp.route('/stats/offer')
def stats_offer():
	form = forms.DateTimeRangeForm(request.args)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		stats, count = rc.offer_stats.list_user(g.user, offset=offset, limit=limit, **form.range_args())
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/stats/offer.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/subid')
@affiliate_only
def stats_sub_id():
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		query_params = dict(aff_id=g.user.id, offset=offset, limit=limit,
			g_sub_id=form.g_sub_id.data, g_sub_id1=form.g_sub_id1.data, g_sub_id2=form.g_sub_id2.data, 
			g_sub_id3=form.g_sub_id3.data, g_sub_id4=form.g_sub_id4.data, **form.range_args())
		if form.sub_id.data: query_params.update(sub_id=form.sub_id.data)
		if form.sub_id1.data: query_params.update(sub_id1=form.sub_id1.data)
		if form.sub_id2.data: query_params.update(sub_id2=form.sub_id2.data)
		if form.sub_id3.data: query_params.update(sub_id3=form.sub_id3.data)
		if form.sub_id4.data: query_params.update(sub_id4=form.sub_id4.data)
		if form.offer.data: query_params.update(offer_id=form.offer.data)
		stats, count = rc.offer_stats.list_by_sub_id(**query_params)
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/stats/sub-id.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/sourceid')
@affiliate_only
def stats_source_id():
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		query_params = dict(aff_id=g.user.id, offset=offset, limit=limit, **form.range_args())
		if form.offer.data: query_params.update(offer_id=form.offer.data)
		stats, count = rc.offer_stats.list_by_source_id(**query_params)
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/stats/source-id.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/referer')
@affiliate_only
def stats_referer():
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		query_params = dict(aff_id=g.user.id, offset=offset, limit=limit, **form.range_args())
		if form.offer.data: query_params.update(offer_id=form.offer.data)
		stats, count = rc.offer_stats.list_by_referer(**query_params)
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/stats/referer.html', stats=stats, pages=pages, form=form)

@bp.route('/stats/keywords')
@affiliate_only
def stats_keywords():
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	if form.validate():
		page = current_page()
		per_page = app.config.get('OFFERS_PER_PAGE', 20)
		offset, limit = page_limits(page, per_page)
		query_params = dict(aff_id=g.user.id, offset=offset, limit=limit, **form.range_args())
		if form.offer.data: query_params.update(offer_id=form.offer.data)
		stats, count = rc.offer_stats.list_by_keywords(**query_params)
		pages = paginate(page, count, per_page)
	else:
		stats, pages = [], None
	return render_template('cabinetcpa/stats/keywords.html', stats=stats, pages=pages, form=form)
	