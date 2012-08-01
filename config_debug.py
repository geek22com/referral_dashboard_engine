# -*- coding: utf-8 -*-
import os

# configuration
DEBUG = True
SECRET_KEY = '47621c2a464441cb94918fa6853c1b0a'
RESTAPI_SERVER = 'http://localhost:5468'
USE_DATABASE = True

SITE_ROOT = 'http://localhost:8989'

# Restkit configuration
RESTKIT_TIMEOUT = 5
RESTKIT_MAX_TRIES = 1
RESTKIT_LOG_LEVEL = 'info'

THIS_PATH = os.path.realpath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(os.path.dirname(THIS_PATH), 'upload')
OFFER_LOGOS_DIR = 'offer-logos'
NEWS_IMAGES_DIR = 'news'

DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_NOSEC_FORMAT = DATETIME_FORMAT[:-3]
DATE_FORMAT = DATETIME_FORMAT.split(' ')[0]
TIME_FORMAT = DATETIME_FORMAT.split(' ')[1]

# Backend parameters
APP_EMAIL = "ks.shilov@gmail.com"

# MailJet API parameters
MAILJET_API_KEY = '807acc36b2f4763cc4e16e8a7b3fa945'
MAILJET_API_SECRET_KEY = 'c8f23ac9200c098f86a4cc5cae42ce19'
MAILJET_API_URL = 'http://api.mailjet.com/0.1'
MAILJET_TIMEOUT = 10
MAILJET_MAX_TRIES = 1
MAILJET_USERS_LIST_ID = 31038
MAILJET_ADVERTISERS_LIST_ID = 31039
MAILJET_AFFILIATES_LIST_ID = 31040

# Mail sending parameters
MAIL_ENABLED = False
MAIL_SMTP_DEBUG = False
MAIL_SMTP_HOST = 'in.mailjet.com'
MAIL_SMTP_PORT = 587 #25
MAIL_SMTP_TIMEOUT = 5
MAIL_SMTP_USERNAME = MAILJET_API_KEY
MAIL_SMTP_PASSWORD = MAILJET_API_SECRET_KEY
MAIL_FROM_ADDRESS = 'HeyMoose! <noreply@heymoose.com>'
MAIL_ADMINS = ['slezko@heymoose.com']

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
CONFIRM_CRYPT_KEY =  'gR7Bsvu46jE623Gg'

BACKEND_BASE_URL = 'http://localhost:5468'
BACKEND_TIMEOUT = 5
BACKEND_MAX_TRIES = 1
BACKEND_BANNERS_PATH = '{0}/banners/local/'.format(BACKEND_BASE_URL)

# Mongo parameters
MONGOALCHEMY_SERVER_AUTH = False
MONGOALCHEMY_DATABASE = 'heymoose'

# Business logic parameters
CURRENCY_SIGN = u'руб.'

# Robokassa parameters
ROBOKASSA_REQUEST_URL = 'https://merchant.roboxchange.com/Index.aspx' # 'http://test.robokassa.ru/Index.aspx'
ROBOKASSA_LOGIN = 'ks.shilov'
ROBOKASSA_PASS1 = 'appatit23843'
ROBOKASSA_USER_PREFIX = 'shp'
ROBOKASSA_DEFAULT_CURRENCY = 'WMRM'
ROBOKASSA_WMID = '276669831570'
