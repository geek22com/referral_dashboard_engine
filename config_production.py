# -*- coding: utf-8 -*-
import os

# configuration
DEBUG = True
SECRET_KEY = '47621c2a464441cb94918fa6853c1b0a'

# Restkit configuration
RESTKIT_TIMEOUT = 60
RESTKIT_MAX_TRIES = 1
RESTKIT_LOG_LEVEL = 'info'

THIS_PATH = os.path.realpath(os.path.dirname(__file__))
UPLOAD_PATH = '/usr/share/nginx/uwsgi_upload'
OFFER_LOGOS_DIR = 'offer-logos'
NEWS_IMAGES_DIR = 'news'

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_NOSEC_FORMAT = DATETIME_FORMAT[:-3]
DATE_FORMAT = DATETIME_FORMAT.split(' ')[0]
TIME_FORMAT = DATETIME_FORMAT.split(' ')[1]

# MailJet API parameters
MAILJET_API_KEY = '807acc36b2f4763cc4e16e8a7b3fa945'
MAILJET_API_SECRET_KEY = 'c8f23ac9200c098f86a4cc5cae42ce19'
MAILJET_API_URL = 'http://api.mailjet.com/0.1'
MAILJET_TIMEOUT = 10
MAILJET_MAX_TRIES = 1
MAILJET_USERS_LIST_ID = 31041
MAILJET_ADVERTISERS_LIST_ID = 31042
MAILJET_AFFILIATES_LIST_ID = 31043
MAILJET_COUNTDOWN_LIST_ID = 86028

# Mail sending parameters
MAIL_ENABLED = True
MAIL_SMTP_DEBUG = False
MAIL_SMTP_HOST = 'in.mailjet.com'
MAIL_SMTP_PORT = 25
MAIL_SMTP_TIMEOUT = 5
MAIL_SMTP_USERNAME = MAILJET_API_KEY
MAIL_SMTP_PASSWORD = MAILJET_API_SECRET_KEY
MAIL_FROM_ADDRESS = 'HeyMoose! <noreply@heymoose.com>'
MAIL_ADMINS = ['admin@heymoose.com']

# Flask-Mail parameters
MAIL_SERVER = MAIL_SMTP_HOST
MAIL_PORT = MAIL_SMTP_PORT
MAIL_TIMEOUT = MAIL_SMTP_TIMEOUT
MAIL_USERNAME = MAIL_SMTP_USERNAME
MAIL_PASSWORD = MAIL_SMTP_PASSWORD
MAIL_SUPPRESS_SEND = not MAIL_ENABLED
MAIL_FAIL_SILENTLY = False
DEFAULT_MAIL_SENDER = MAIL_FROM_ADDRESS

# Flask-Assets parameters
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False

# Encryption parameters
REFERRAL_CRYPT_KEY = 'aGy3iRn7fRbIw4yM' # Must be 16 bytes long
CONFIRM_CRYPT_KEY  = 'gR7Bsvu46jE623Gg'

# Backend parameters
BACKEND_BASE_URL = 'http://localhost:5468'
BACKEND_TIMEOUT = 60
BACKEND_MAX_TRIES = 1

TRACKER_BASE_URL = 'http://partner.heymoose.com'
TRACKER_API_URL = TRACKER_BASE_URL + '/api'
TRACKER_BANNERS_URL = TRACKER_BASE_URL + '/pub/banners/'

# Mongo parameters
MONGOALCHEMY_SERVER_AUTH = False
MONGOALCHEMY_DATABASE = 'heymoose'

# Business logic parameters
CURRENCY_SIGN = u'руб.'
WOMEN_CATEGORIES = (43, 44, 45, 46, 47)

# Robokassa parameters
ROBOKASSA_REQUEST_URL = 'https://merchant.roboxchange.com/Index.aspx' #'http://test.robokassa.ru/Index.aspx'
ROBOKASSA_LOGIN = 'ks.shilov'
ROBOKASSA_PASS1 = 'appatit23843'
ROBOKASSA_USER_PREFIX = 'shp'
ROBOKASSA_DEFAULT_CURRENCY = 'WMRM'
ROBOKASSA_WMID = '276669831570'

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

LOGGER_NAME = 'heymoose'
LOGGING = {
	'version' : 1,
	'disable_existing_loggers' : False,
	'formatters' : {
		'common' : {
			'format' : '%(asctime)s %(levelname)-7s %(message)s',
			#'datefmt' : '%H:%M:%S'
		},
	},
	'handlers' : {
		'console' : {
			'level' : 'DEBUG' if DEBUG else 'INFO',
			'class' : 'logging.StreamHandler',
			'formatter' : 'common'
		},
	},
	'loggers' : {
		'heymoose' : {
			'handlers' : ['console'],
			'level' : 'DEBUG' if DEBUG else 'INFO',
		}
	}
}
