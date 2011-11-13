from datetime import datetime

def datetime_from_api(dt):
	return datetime.strptime(dt[:-6], '%Y-%m-%dT%H:%M:%S.%f')


def to_int(value, default=0):
	try:
		return int(value)
	except:
		return default