from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY
# Do not remove unused imports here! They are used from other modules.

def begin_of_minute(d):
	return d.replace(microsecond=0, second=0)

def end_of_minute(d):
	return begin_of_minute(d) + relativedelta(minutes=+1, microseconds=-1)

def begin_of_hour(d):
	return d.replace(microsecond=0, second=0, minute=0)

def end_of_hour(d):
	return begin_of_hour(d) + relativedelta(hours=+1, microseconds=-1)

def begin_of_day(d):
	return d.replace(microsecond=0, second=0, minute=0, hour=0)

def end_of_day(d):
	return begin_of_day(d) + relativedelta(days=+1, microseconds=-1)

def begin_of_month(d):
	return d.replace(microsecond=0, second=0, minute=0, hour=0, day=1)

def end_of_month(d):
	return begin_of_month(d) + relativedelta(months=+1, microseconds=-1)


def delta(value, **kwargs):
	return value + relativedelta(**kwargs)


def datetime_range(freq, **kwargs):
	return list(rrule(freq, **kwargs))