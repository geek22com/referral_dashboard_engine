from wtforms.validators import NumberRange, Required, Regexp
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