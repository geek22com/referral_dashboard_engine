# -*- coding: utf-8 -*-
from flask import request
from heymoose import resource as rc
from heymoose.forms import forms
from heymoose.admin import blueprint as bp
from heymoose.views.decorators import template, sorted, paginated
from heymoose.utils.config import config_accessor


OFFER_STATS_PER_PAGE = config_accessor('OFFER_STATS_PER_PAGE', 20)
AFFILIATE_STATS_PER_PAGE = config_accessor('AFFILIATE_STATS_PER_PAGE', 20)
ADVERTISER_STATS_PER_PAGE = config_accessor('ADVERTISER_STATS_PER_PAGE', 20)


@bp.route('/stats/offer')
@template('admin/stats/offer.html')
@sorted('clicks_count', 'desc')
@paginated(OFFER_STATS_PER_PAGE)
def stats_offer(**kwargs):
	form = forms.OfferStatsFilterForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_all(**kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/affiliate')
@template('admin/stats/affiliate.html')
@sorted('clicks_count', 'desc')
@paginated(AFFILIATE_STATS_PER_PAGE)
def stats_affiliate(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_affiliate(**kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/advertiser')
@template('admin/stats/advertiser.html')
@sorted('clicks_count', 'desc')
@paginated(ADVERTISER_STATS_PER_PAGE)
def stats_advertiser(**kwargs):
	form = forms.DateTimeRangeForm(request.args)
	kwargs.update(form.backend_args())
	stats, count = rc.offer_stats.list_advertiser(**kwargs) if form.validate() else ([], 0)
	return dict(stats=stats, count=count, form=form)

@bp.route('/stats/total')
@template('admin/stats/total.html')
def stats_total():
	form = forms.DateTimeRangeForm(request.args)
	stats = rc.offer_stats.total(**form.backend_args()) if form.validate() else []
	return dict(stats=stats, form=form)
