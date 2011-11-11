from heymoose import app
import base64

def error_type(value, type):
	return filter(lambda x: x[0] == type, value)
app.jinja_env.filters['error_type'] = error_type


def datetimeformat(value, format='%d.%m.%Y %H:%M:%S'):
	return value.strftime(format)
app.jinja_env.filters['datetimeformat'] = datetimeformat


def dateformat(value, format='%d.%m.%Y'):
	return value.strftime(format)
app.jinja_env.filters['dateformat'] = dateformat


def timeformat(value, format='%H:%M:%S'):
	return value.strftime(format)
app.jinja_env.filters['timeformat'] = timeformat


def base64filter(value):
	return base64.encodestring(value).strip('\n')
app.jinja_env.filters['base64filter'] = base64filter

