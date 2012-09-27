from heymoose import app
import time
import calendar


datetime_format = app.config.get('DATETIME_FORMAT', '%d.%m.%Y %H:%M:%S')
datetime_nosec_format = app.config.get('DATETIME_NOSEC_FORMAT', '%d.%m.%Y %H:%M')


def to_unixtime(value, msec=False):
	result = int(time.mktime(value.timetuple()))
	return result * 1000 if msec else result

def to_unixtime_utc(value):
	return calendar.timegm(value.timetuple())
