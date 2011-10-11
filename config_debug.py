# configuration
DEBUG = True
SECRET_KEY = 'lola pola_mola_cola'
RESTAPI_SERVER = 'http://localhost:5468'
USE_DATABASE = True

APP_ID = "243934035656884"
APP_SECRET = "054cec4abf69a4dd6fcaa4b75cd04f01"
DEVELOPER_SECRET_KEY = "3ca2a85b953ffef29625ffc11df61eee"

#backend parameters
APP_EMAIL = "ks.shilov@gmail.com"

#Facebook parameters
FACEBOOK_SERVICE_URL = "http://www.facebook.com"
FACEBOOK_GRAPH_URL = "https://graph.facebook.com"
FACEBOOK_APP_DOMAIN = "http://heymoose.com:8090"
FACEBOOK_APP_URL = "http://apps.facebook.com/heymoose_debug/"
FACEBOOK_AUTH_SCOPE = "publish_stream,email,create_event,sms,publish_actions,user_likes,user_about_me"

BACKEND_PRIVATE_URL = "http://localhost"
BACKEND_PRIVATE_PORT = 1234

#Mongo parameters
MONGOALCHEMY_SERVER_AUTH = False
MONGOALCHEMY_DATABASE = 'facebook_debug'

print "ATTENTION!! DEBUG CONFIG IS USED"
