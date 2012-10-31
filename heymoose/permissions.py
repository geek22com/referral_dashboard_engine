# -*- coding: utf-8 -*-

# Admin permissions parameters
SUPER_ADMINS = ['admin@heymoose.com']
ADMIN_GROUPS = {
	u'Сверки': set([
		'view_advertiser',
		'view_advertiser_offers',
		'view_advertiser_finances',
		'view_advertiser_stats',
		'view_offer_sales',
		'view_offer_stats'
	]),
	u'Поддержка рекламодателей': set([
		'view_advertiser',
		'view_advertiser_offers',
		'view_advertiser_finances',
		'view_advertiser_stats',
		'do_advertiser_edit',
		'do_advertiser_login',
		'do_advertiser_block',
		'view_offer_sales',
		'view_offer_requests',
		'view_offer_stats',
		'do_offer_edit',
	]),
	u'Поддержка партнёров': set([
		'view_fraud',
		'view_affiliate',
		'view_affiliate_offers',
		'view_affiliate_finances',
		'view_affiliate_referrals',
		'view_affiliate_stats',
		'do_affiliate_edit',
		'do_affiliate_login',
		'do_affiliate_block',
		'view_offer_requests'
	]),
	u'Анализ трафика': set([
		'view_fraud',
		'view_affiliate',
		'view_affiliate_offers',
		'view_affiliate_stats',
		'do_affiliate_block',
		'view_offer_requests',
		'view_offer_stats'
	]),
	u'PR': set([
		'view_affiliate',
		'view_affiliate_offers',
		'view_advertiser',
		'view_advertiser_offers'
	])
}