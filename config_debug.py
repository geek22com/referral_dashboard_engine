# -*- coding: utf-8 -*-
import os

# configuration
DEBUG = True
SECRET_KEY = 'lola pola_mola_cola'
RESTAPI_SERVER = 'http://localhost:5468'
USE_DATABASE = True

# Restkit configuration
RESTKIT_TIMEOUT = 5
RESTKIT_MAX_TRIES = 1
RESTKIT_LOG_LEVEL = 'info'

THIS_PATH = os.path.realpath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(os.path.dirname(THIS_PATH), 'upload')

APP_ID = "243934035656884"
APP_SECRET = "054cec4abf69a4dd6fcaa4b75cd04f01"
DEVELOPER_SECRET_KEY = "3ca2a85b953ffef29625ffc11df61eee"

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_NOSEC_FORMAT = DATETIME_FORMAT[:-3]
DATE_FORMAT = DATETIME_FORMAT.split(' ')[0]
TIME_FORMAT = DATETIME_FORMAT.split(' ')[1]

# Backend parameters
APP_EMAIL = "ks.shilov@gmail.com"

# Admin parameters
ADMIN_PAGES_RANGE = 7
ADMIN_USERS_PER_PAGE = 20
ADMIN_ORDERS_PER_PAGE = 20
ADMIN_APPS_PER_PAGE = 20
ADMIN_ACTIONS_PER_PAGE = 40
ADMIN_PERFORMERS_PER_PAGE = 40
ADMIN_TRANSACTIONS_PER_PAGE = 20

# Encryption parameters
REFERRAL_CRYPT_KEY = 'aGy3iRn7fRbIw4yM' # Must be 16 bytes long

# Facebook parameters
FACEBOOK_SERVICE_URL = "http://www.facebook.com"
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"
FACEBOOK_APP_DOMAIN = "http://heymoose.com:8090"
FACEBOOK_APP_URL = "http://apps.facebook.com/heymoose_debug/"
FACEBOOK_AUTH_SCOPE = "publish_stream,email,create_event,sms,publish_actions,user_likes,user_about_me"

BACKEND_PRIVATE_URL = "http://localhost"
BACKEND_PRIVATE_PORT = 1234

# Mongo parameters
MONGOALCHEMY_SERVER_AUTH = False
MONGOALCHEMY_DATABASE = 'facebook_debug'

# Business logic parameters
REFERRAL_MIN_CPC = 5.0
REFERRAL_RECOMMENDED_CPC_QUOT = 1.3
CURRENCY_SIGN = u'у.е.'

# Robokassa parameters
ROBOKASSA_REQUEST_URL = 'http://test.robokassa.ru/Index.aspx'
ROBOKASSA_LOGIN = 'ks.shilov'
ROBOKASSA_PASS1 = 'appatit23843'
ROBOKASSA_USER_PREFIX = 'shp_'
ROBOKASSA_DEFAULT_CURRENCY = 'WMRM'
ROBOKASSA_WMID = '276669831570'

print "ATTENTION!! DEBUG CONFIG IS USED"
