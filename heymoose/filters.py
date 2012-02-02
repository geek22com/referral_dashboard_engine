# -*- coding: utf-8 -*-
from heymoose import app
from heymoose.utils import times, convert
from datetime import datetime
import base64

currency_sign = app.config.get('CURRENCY_SIGN')
site_root = app.config.get('SITE_ROOT', 'http://www.heymoose.com')

def error_type(value, type):
	return filter(lambda x: x[0] == type, value) if value else None


def datetimeformat(value, format=convert.datetime_format):
	return value.strftime(format) if value else None


def datetime_nosec(value, format=convert.datetime_nosec_format):
	return value.strftime(format) if value else None


def dateformat(value, format='%d.%m.%Y'):
	return value.strftime(format) if value else None


def timeformat(value, format='%H:%M:%S'):
	return value.strftime(format) if value else None


def base64filter(value):
	return base64.encodestring(value).strip('\n') if value else None


def addclass(value, cls):
	if 'class' not in value:
		value['class'] = cls
	else:
		value['class'] += ' ' + cls;
	return ''


def classname(value):
	return value.__class__.__name__ if value else None


def attrlist(values, attr):
	return [getattr(value, attr) for value in values]


def currency(value, sign=True):
	return (u'%.2f' % value) + (u' ' + currency_sign if sign else u'')


def replace_if_contains(value, contains, newvalue):
	if value and contains in value:
		return newvalue
	return value


app.jinja_env.filters['error_type'] = error_type
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['datetime_nosec'] = datetime_nosec
app.jinja_env.filters['dateformat'] = dateformat
app.jinja_env.filters['timeformat'] = timeformat
app.jinja_env.filters['base64filter'] = base64filter
app.jinja_env.filters['addclass'] = addclass
app.jinja_env.filters['classname'] = classname
app.jinja_env.filters['attrlist'] = attrlist
app.jinja_env.filters['delta'] = times.delta
app.jinja_env.filters['currency'] = currency
app.jinja_env.filters['replace_if_contains'] = replace_if_contains

app.jinja_env.globals['now'] = datetime.now
app.jinja_env.globals['currency_sign'] = currency_sign
app.jinja_env.globals['root'] = site_root
