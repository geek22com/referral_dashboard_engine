# -*- coding: utf-8 -*-
import os
from heymoose.config_default import *

# Flask parameters
DEBUG = False
TESTING = False
SECRET_KEY = '47621c2a464441cb94918fa6853c1b0a'

# Dirs configuration
THIS_PATH = os.path.realpath(os.path.dirname(__file__))
UPLOAD_PATH = '/usr/share/nginx/uwsgi_upload'
OFFER_LOGOS_DIR = 'offer-logos'
NEWS_IMAGES_DIR = 'news'

# MailJet API parameters
MAILJET_USERS_LIST_ID = 31041
MAILJET_ADVERTISERS_LIST_ID = 31042
MAILJET_AFFILIATES_LIST_ID = 31043
MAILJET_COUNTDOWN_LIST_ID = 86028

# Mail sending parameters
MAIL_ENABLED = True
MAIL_SMTP_PORT = 25
MAIL_ADMINS = ['admin@heymoose.com']

# Flask-Mail parameters
MAIL_SUPPRESS_SEND = not MAIL_ENABLED
MAIL_PORT = MAIL_SMTP_PORT

# Flask-Assets parameters
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False

# Backend parameters
BACKEND_TIMEOUT = 60
TRACKER_BASE_URL = 'http://partner.heymoose.com'
TRACKER_API_URL = TRACKER_BASE_URL + '/api'
TRACKER_BANNERS_URL = TRACKER_BASE_URL + '/pub/banners/'

