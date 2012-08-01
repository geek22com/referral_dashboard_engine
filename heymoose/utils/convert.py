from datetime import datetime
from heymoose.utils.config import config_value
import time
import calendar

def datetime_from_api(dt):
	if dt is None: return None
	without_tz = dt[:-1] if dt.endswith('Z') else dt[:-6]
	return datetime.strptime(without_tz, '%Y-%m-%dT%H:%M:%S.%f')

def datetime_from_unixtime(dt, msec=False):
	if dt is None: return None
	return datetime.fromtimestamp(dt / 1000 if msec else dt)

def to_datetime(value):
	format = config_value('DATETIME_FORMAT', '%d.%m.%Y %H:%M:%S')
	return datetime.strptime(str(value), format)

def to_unixtime(value, msec=False):
	result = int(time.mktime(value.timetuple()))
	return result * 1000 if msec else result

def to_unixtime_utc(value):
	return calendar.timegm(value.timetuple())


def to_int(value, default=0):
	try:
		return int(value)
	except:
		return default
	
	
def to_bool(value, empty_is_none=True):
	if isinstance(value, bool): return value
	if not value:
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
			