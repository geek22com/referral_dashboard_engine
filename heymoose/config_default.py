# -*- coding: utf-8 -*-

# Flask parameters
DEBUG = False
TESTING = False
SECRET_KEY = None

# Dirs configuration
UPLOAD_PATH = None
OFFER_LOGOS_DIR = None
NEWS_IMAGES_DIR = None

# Date and time parameters
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
MAILJET_USERS_LIST_ID = 31038
MAILJET_ADVERTISERS_LIST_ID = 31039
MAILJET_AFFILIATES_LIST_ID = 31040
MAILJET_COUNTDOWN_LIST_ID = 86030

# Mail sending parameters
MAIL_ENABLED = False
MAIL_SMTP_HOST = 'in.mailjet.com'
MAIL_SMTP_PORT = 25 # May be 587, 25, 465
MAIL_SMTP_TIMEOUT = 5
MAIL_SMTP_USERNAME = MAILJET_API_KEY
MAIL_SMTP_PASSWORD = MAILJET_API_SECRET_KEY
MAIL_FROM_ADDRESS = 'HeyMoose! <noreply@heymoose.com>'
MAIL_ADMINS = ['slezko@heymoose.com']

# Flask-Mail parameters
MAIL_SERVER = MAIL_SMTP_HOST
MAIL_PORT = MAIL_SMTP_PORT
MAIL_TIMEOUT = MAIL_SMTP_TIMEOUT
MAIL_USERNAME = MAIL_SMTP_USERNAME
MAIL_PASSWORD = MAIL_SMTP_PASSWORD
MAIL_USE_SSL = False
MAIL_SUPPRESS_SEND = not MAIL_ENABLED
MAIL_FAIL_SILENTLY = False
DEFAULT_MAIL_SENDER = MAIL_FROM_ADDRESS

# Flask-Assets parameters
ASSETS_DEBUG = True
ASSETS_AUTO_BUILD = True

# Flask-MongoAlchemy parameters
MONGOALCHEMY_SERVER_AUTH = False
MONGOALCHEMY_DATABASE = 'heymoose'

# Encryption parameters
REFERRAL_CRYPT_KEY = 'aGy3iRn7fRbIw4yM' # Must be 16 bytes long
CONFIRM_CRYPT_KEY =  'gR7Bsvu46jE623Gg'

# Backend parameters
BACKEND_BASE_URL = 'http://localhost:5468'
BACKEND_TIMEOUT = 15
BACKEND_MAX_TRIES = 1
TRACKER_BASE_URL = BACKEND_BASE_URL
TRACKER_API_URL = TRACKER_BASE_URL + '/api'
TRACKER_BANNERS_URL = TRACKER_BASE_URL + '/banners/local/'

# Business logic parameters
CURRENCY_SIGN = u'руб.'
WOMEN_CATEGORIES = (43, 44, 45, 46, 47)

# Robokassa parameters
ROBOKASSA_REQUEST_URL = 'https://merchant.roboxchange.com/Index.aspx' # 'http://test.robokassa.ru/Index.aspx'
ROBOKASSA_LOGIN = 'ks.shilov'
ROBOKASSA_PASS1 = 'appatit23843'
ROBOKASSA_USER_PREFIX = 'shp'
ROBOKASSA_DEFAULT_CURRENCY = 'WMRM'
ROBOKASSA_WMID = '276669831570'

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

from permissions import *