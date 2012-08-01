# -*- coding: utf-8 -*-
from flask import request, g
from heymoose import resource as rc
from heymoose.forms import forms
from heymoose.utils.config import config_accessor
from heymoose.views.decorators import template, sorted, paginated
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only

OFFER_STATS_PER_PAGE = config_accessor('OFFER_STATS_PER_PAGE', 20)
SUB_ID_STATS_PER_PAGE = config_accessor('SUB_ID_STATS_PER_PAGE', 20)
SOURCE_ID_STATS_PER_PAGE = config_accessor('SOURCE_ID_STATS_PER_PAGE', 20)
REFERER_STATS_PER_PAGE = config_accessor('REFERER_STATS_PER_PAGE', 20)
KEYWORDS_STATS_PER_PAGE = config_accessor('KEYWORDS_STATS_PER_PAGE', 20)


@bp.route('/stats/offer')
@template('cabinetcpa/stats/offer.html')
@sorted('clicks_count', 'desc')
@paginated(OFFER_STATS_PER_PAGE)
def stats_offer(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_user(g.user, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/subid')
@affiliate_only
@template('cabinetcpa/stats/sub-id.html')
@sorted('clicks_count', 'desc')
@paginated(SUB_ID_STATS_PER_PAGE)
def stats_sub_id(**kwargs):
	offers, _ = rc.offers.list_requested(g.user.id, offset=0, limit=100000)
	form = forms.AffiliateCabinetSubIdStatsForm(request.args)
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
	form = forms.AffiliateCabinetStatsForm(request.args)
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
	form = forms.AffiliateCabinetStatsForm(request.args)
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
	form = forms.AffiliateCabinetStatsForm(request.args)
	form.offer.set_offers(offers)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_by_keywords(aff_id=g.user.id, **kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)
