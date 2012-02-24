# -*- coding: utf-8 -*-
from wtforms import ValidationError
from wtforms.validators import NumberRange, Required, Regexp
from heymoose.core import actions
from heymoose.db.actions import invites
from heymoose.utils.gen import check_password_hash
import re, urllib, urllib2

class NumberRangeEx(NumberRange):
	'''NumberRange validator which allows empty value'''
	
	def __call__(self, form, field):
		if field.data is None: return
		super(NumberRangeEx, self).__call__(form, field)
		
		
class FileRequired(Required):
	'''Required validator for FileField'''
	
	def __call__(self, form, field):
		value = field.data
		if field.process_errors: return
		if value is not None and hasattr(value, 'filename') and value.filename: return
		super(FileRequired, self).__call__(form, field)
		
		
class URLWithParams(Regexp):
	'''Validator for string representing URL with GET-parameters'''
	
	def __init__(self, message=None):
		regex = ur'^(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$'
		super(URLWithParams, self).__init__(regex, re.IGNORECASE, message)

	def __call__(self, form, field):
		if self.message is None:
			self.message = field.gettext(u'Invalid URL')

		super(URLWithParams, self).__call__(form, field)


class URI(Regexp):
	'''Validator for string representing URI'''
	
	def __init__(self, verify_exists=True, message=None):
		self.verify_exists = verify_exists
		
		regex = r'^(?:http)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$'
		
		super(URI, self).__init__(regex, re.IGNORECASE, message)

	def __call__(self, form, field):
		super(URI, self).__call__(form, field)
		url = field.data
		
		if self.verify_exists:
			headers = {
				"Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
				"Accept-Language": "en-us,en;q=0.5",
				"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
				"Connection": "close",
				"User-Agent": "Mozilla/5.0 (Windows; I; Windows NT 5.1; ru; rv:1.9.2.13) Gecko/20100101 Firefox/4.0",
			}
			url = url.encode('utf-8')
			url = urllib.quote(url, "!*'();:@&=+$,/?#[]")
			try:
				req = urllib2.Request(url, None, headers)
				req.get_method = lambda: 'HEAD'
				# Create an opener that does not support local file access
				opener = urllib2.OpenerDirector()

				# Don't follow redirects, but don't treat them as errors either
				error_nop = lambda *args, **kwargs: True
				http_error_processor = urllib2.HTTPErrorProcessor()
				http_error_processor.http_error_301 = error_nop
				http_error_processor.http_error_302 = error_nop
				http_error_processor.http_error_307 = error_nop

				handlers = [urllib2.UnknownHandler(),
							urllib2.HTTPHandler(),
							urllib2.HTTPDefaultErrorHandler(),
							urllib2.HTTPSHandler(),
							http_error_processor]
				map(opener.add_handler, handlers)
				opener.open(req, timeout=10)
			except ValueError:
				raise ValidationError(u'Введите правильный URL')
			except: # urllib2.URLError, httplib.InvalidURL, etc.
				raise ValidationError(u'Похоже, что указанная ссылка битая')
		
		
class FileFormat(object):
	def __init__(self, formats=('jpg', 'jpeg', 'gif', 'png'), message=None):
		self.message = message
		self.formats = formats
		
	def __call__(self, form, field):
		if field.data is None: return
		if self.message is None:
			self.message = field.gettext(u'Invalid image format')
			
		if field.format not in self.formats:
			raise ValidationError(self.message)
		
		
def check_email_not_registered(form, field):
	if actions.users.get_user_by_email(field.data) is not None:
		raise ValidationError(u'Пользователь с таким e-mail уже существует')
	
	
def check_invite(form, field):
	if invites.get_invite(field.data) is None:
		raise ValidationError(u'Неверный код приглашения')


def check_password(form, field):
	if not hasattr(field, 'user') or not check_password_hash(field.user.password_hash, field.data):
		raise ValidationError(u'Неверный пароль')
		
		