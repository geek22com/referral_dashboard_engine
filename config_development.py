# -*- coding: utf-8 -*-
import os
from heymoose.config_default import *

# Flask parameters
DEBUG = True
TESTING = False
SECRET_KEY = '47621c2a464441cb94918fa6853c1b0a'

# Dirs configuration
THIS_PATH = os.path.realpath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(os.path.dirname(THIS_PATH), 'upload')
OFFER_LOGOS_DIR = 'offer-logos'
NEWS_IMAGES_DIR = 'news'

# MailJet API parameters
MAILJET_USERS_LIST_ID = 31038
MAILJET_ADVERTISERS_LIST_ID = 31039
MAILJET_AFFILIATES_LIST_ID = 31040
MAILJET_COUNTDOWN_LIST_ID = 86030

# Mail sending parameters
MAIL_ENABLED = False
MAIL_SMTP_PORT = 465
MAIL_ADMINS = ['slezko@heymoose.com']

# Flask-Mail parameters
MAIL_SUPPRESS_SEND = not MAIL_ENABLED
MAIL_PORT = MAIL_SMTP_PORT

# Flask-Assets parameters
ASSETS_DEBUG = True
ASSETS_AUTO_BUILD = True

# Backend parameters
BACKEND_TIMEOUT = 15