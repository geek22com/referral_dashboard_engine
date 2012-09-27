# -*- coding: utf-8 -*-
from heymoose import app
from heymoose.utils import convert
from datetime import datetime
import base64, time, random


currency_sign = app.config.get('CURRENCY_SIGN')


def datetimeformat(value, format=convert.datetime_format):
	return value.strftime(format) if value else None


def datetime_nosec(value, format=convert.datetime_nosec_format):
	return value.strftime(format) if value else None


def dateformat(value, format='%d.%m.%Y'):
	return value.strftime(format) if value else None


def timeformat(value, format='%H:%M:%S'):
	return value.strftime(format) if value else None


def classname(value):
	return value.__class__.__name__ if value else None


def attrlist(values, attr):
	return [getattr(value, attr) for value in values]


def itemlist(values, index):
	return [value[index] for value in values]


def currency(value, sign=True):
	return (u'%.2f' % float(value)) + (u' ' + currency_sign if sign else u'')


def percent(value, sign=True, multiply=False):
	return (u'%.2f' % (float(value) * 100.0 if multiply else float(value))) + (u' %' if sign else u'')


def updated(dictionary, **kwargs):
	d = dict(dictionary.items())
	d.update(kwargs)
	return d

def nocache():
	return random.randrange(1000000)


app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['datetime_nosec'] = datetime_nosec
app.jinja_env.filters['dateformat'] = dateformat
app.jinja_env.filters['timeformat'] = timeformat
app.jinja_env.filters['classname'] = classname
app.jinja_env.filters['attrlist'] = attrlist
app.jinja_env.filters['itemlist'] = itemlist
app.jinja_env.filters['currency'] = currency
app.jinja_env.filters['percent'] = percent
app.jinja_env.filters['updated'] = updated

app.jinja_env.globals['now'] = datetime.now
app.jinja_env.globals['time'] = time.time
app.jinja_env.globals['currency_sign'] = currency_sign
app.jinja_env.globals['nocache'] = nocache
