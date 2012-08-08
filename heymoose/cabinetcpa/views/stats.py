# -*- coding: utf-8 -*-
from flask import request, g, redirect, url_for
from heymoose import app, resource as rc
from heymoose.forms import forms
from heymoose.views.decorators import template, sorted, paginated
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only, advertiser_only

OFFER_STATS_PER_PAGE = app.config.get('OFFER_STATS_PER_PAGE', 20)
AFFILIATE_STATS_PER_PAGE = app.config.get('AFFILIATE_STATS_PER_PAGE', 20)
SUB_ID_STATS_PER_PAGE = app.config.get('SUB_ID_STATS_PER_PAGE', 20)
SOURCE_ID_STATS_PER_PAGE = app.config.get('SOURCE_ID_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = app.config.get('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = app.config.get('KEYWORDS_STATS_PER_PAGE', 20)
SUBOFFER_STATS_PER_PAGE = app.config.get('SUBOFFER_STATS_PER_PAGE', 20)


@bp.route('/stats/offer')
@template('cabinetcpa/stats/offer.html')
@sorted('clicks_count', 'desc')
@paginated(OFFER_STATS_PER_PAGE)
def stats_offer(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_user(g.user, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/affiliate')
@advertiser_only
@template('cabinetcpa/stats/affiliate.html')
@sorted('clicks_count', 'desc')
@paginated(AFFILIATE_STATS_PER_PAGE)
def stats_affiliate(**kwargs):
	offers, _ = rc.offers.list(advertiser_id=g.user.id, offset=0, limit=100000)
	if not offers: return redirect(url_for('.stats_offer'))
	form = forms.CabinetStatsForm(request.args, offer=offers[0].id)
	form.offer.set_offers(offers, empty=None)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_affiliate_by_offer(for_advertiser=True, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/subid')
@affiliate_only
@template('cabinetcpa/stats/sub-id.html')
@sorted('clicks_count', 'desc')
@paginated(SUB_ID_STATS_PER_PAGE)
def stats_sub_id(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_sub_id(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/sourceid')
@affiliate_only
@template('cabinetcpa/stats/source-id.html')
@sorted('clicks_count', 'desc')
@paginated(SOURCE_ID_STATS_PER_PAGE)
def stats_source_id(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_source_id(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/referer')
@affiliate_only
@template('cabinetcpa/stats/referer.html')
@sorted('clicks_count', 'desc')
@paginated(REFERER_STATS_PER_PAGE)
def stats_referer(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_referer(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/keywords')
@affiliate_only
@template('cabinetcpa/stats/keywords.html')
@sorted('clicks_count', 'desc')
@paginated(KEYWORDS_STATS_PER_PAGE)
def stats_keywords(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/suboffer')
@affiliate_only
@template('cabinetcpa/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def stats_suboffer(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_suboffer(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)

@bp.route('/stats/suboffer/sub_id')
@affiliate_only
@template('cabinetcpa/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def stats_suboffer_sub_id(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetSubIdStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	kwargs.update(form.sub_ids_from_string(request.args.get('sub_ids')))
	stats, count = rc.offer_stats.list_suboffer_by_sub_id(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)

@bp.route('/stats/suboffer/source_id')
@affiliate_only
@template('cabinetcpa/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def stats_suboffer_source_id(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(source_id=request.args.get('source_id'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_source_id(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)

@bp.route('/stats/suboffer/referer')
@affiliate_only
@template('cabinetcpa/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def stats_suboffer_referer(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(referer=request.args.get('referer'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_referer(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)

@bp.route('/stats/suboffer/keywords')
@affiliate_only
@template('cabinetcpa/stats/suboffer.html')
@sorted('leads_count', 'desc')
@paginated(SUBOFFER_STATS_PER_PAGE)
def stats_suboffer_keywords(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.CabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(keywords=request.args.get('keywords'), **form.backend_args())
	stats, count = rc.offer_stats.list_suboffer_by_keywords(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, offer=form.offer.selected)
