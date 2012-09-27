# -*- coding: utf-8 -*-
from wtforms import ValidationError
from wtforms import validators as wtvalidators
from heymoose import resource as rc
from heymoose.utils.gen import check_password_hash
from heymoose.utils.dicts import create_dict
import re, urllib, urllib2


class Optional(wtvalidators.Optional):
	css_class = 'validate-optional'


class Required(wtvalidators.Required):
	css_class = 'validate-required'
	
	def data_attrs(self):
		return create_dict(**{'data-required-message': self.message or None})


class FileRequired(Required):
	'''Required validator for FileField'''
	
	def __call__(self, form, field):
		value = field.data
		if field.process_errors: return
		if value is not None and hasattr(value, 'filename') and value.filename: return
		super(FileRequired, self).__call__(form, field)


class NumberRange(wtvalidators.NumberRange):
	css_class = 'validate-range'
	
	def data_attrs(self):
		return create_dict(**{
			'data-range-message': self.message or None,
			'data-range-min': self.min or None,
			'data-range-max': self.max or None
		})


class NumberRangeOptional(NumberRange):
	'''NumberRange validator which allows empty value'''
	
	def __call__(self, form, field):
		if field.data is None: return
		super(NumberRangeOptional, self).__call__(form, field)


class Length(wtvalidators.Length):
	css_class = 'validate-length'
	
	def data_attrs(self):
		return create_dict(**{
			'data-length-message': self.message or None,
			'data-length-min': self.min or None,
			'data-length-max': self.max or None
		})


class EqualTo(wtvalidators.EqualTo):
	css_class = 'validate-equal'
	
	def data_attrs(self):
		return create_dict(**{
			'data-equal-message': self.message or None,
			'data-equal-other': self.fieldname or None
		})


class Email(wtvalidators.Email):
	pass
		

class Decimal(object):
	css_class = 'validate-decimal'
	field_flags = ('required', )
	
	def __init__(self, message=None):
		self.message = message
		
	def __call__(self, form, field):
		pass
	
	def data_attrs(self):
		return create_dict(**{'data-decimal-message': self.message or None})

class Integer(object):
	css_class = 'validate-integer'
	field_flags = ('required', )
	
	def __init__(self, message=None):
		self.message = message
		
	def __call__(self, form, field):
		pass
	
	def data_attrs(self):
		return create_dict(**{'data-integer-message': self.message or None})


class URLWithParams(wtvalidators.Regexp):
	'''Validator for string representing URL with GET-parameters'''
	
	css_class = 'validate-url'
	
	def __init__(self, message=None):
		regex = ur'^(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?$'
		super(URLWithParams, self).__init__(regex, re.IGNORECASE, message)
		
	def data_attrs(self):
		return create_dict(**{'data-url-message': self.message or None})


class URI(wtvalidators.Regexp):
	'''Validator for string representing URI'''
	
	css_class = 'validate-url'
	
	def __init__(self, verify_exists=True, message=None):
		self.verify_exists = verify_exists
		
		regex = r'^(?:http)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$'
		
		super(URI, self).__init__(regex, re.IGNORECASE, message)

	def __call__(self, form, field):
		if not field.data: return
		super(URI, self).__call__(form, field)
		url = field.data
		
		if url.strip() == 'http://':
			raise ValidationError(self.message)
		
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
	
	def data_attrs(self):
		return create_dict(**{'data-url-message': self.message or None})


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
	if rc.users.get_by_email_safe(field.data) is not None:
		raise ValidationError(u'Пользователь с таким e-mail уже существует')
	
	
def check_password(form, field):
	if not form.user or not check_password_hash(form.user.password_hash, field.data):
		raise ValidationError(u'Неверный пароль')
		
		