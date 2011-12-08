# -*- coding: utf-8 -*-
from wtforms import ValidationError
from wtforms.validators import NumberRange, Required, Regexp
from heymoose.core import actions
from heymoose.db.actions import invites
from heymoose.utils.gen import check_password_hash
import re

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
		
		
class ImageFormat(object):
	def __init__(self, formats=('jpg', 'jpeg', 'gif', 'png'), message=None):
		self.message = message
		self.formats = formats
		
	def __call__(self, form, field):
		if field.data is None: return
		if self.message is None:
			self.message = field.gettext(u'Invalid image format')
			
		if field.data.format.lower() not in self.formats:
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
		
		