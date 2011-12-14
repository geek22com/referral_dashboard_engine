from datetime import datetime
from heymoose import app
import time
import calendar

datetime_format = app.config.get('DATETIME_FORMAT', '%d.%m.%Y %H:%M:%S')
datetime_nosec_format = app.config.get('DATETIME_NOSEC_FORMAT', '%d.%m.%Y %H:%M')

def datetime_from_api(dt):
	if dt is None: return None
	without_tz = dt[:-1] if dt.endswith('Z') else dt[:-6]
	return datetime.strptime(without_tz, '%Y-%m-%dT%H:%M:%S.%f')

def to_datetime(value):
	return datetime.strptime(str(value), datetime_format)

def to_unixtime(value):
	return int(time.mktime(value.timetuple()))

def to_unixtime_utc(value):
	return calendar.timegm(value.timetuple())


def to_int(value, default=0):
	try:
		return int(value)
	except:
		return default
	
	
def to_bool(value, empty_is_none=True):
	if value == '' or value == u'':
		return None if empty_is_none else False
	if value.lower() == 'true': return True
	if value.lower() == 'false': return False
	return True


def to_camel_case(value):
	chars = list(value)
	n = len(chars)
	for i, char in enumerate(chars):
		if char == '_' and i != n-1:
			chars[i+1] = chars[i+1].upper()
	return ''.join(chars).replace('_', '')
			