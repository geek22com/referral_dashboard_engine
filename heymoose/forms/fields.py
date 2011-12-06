# -*- coding: utf-8 -*-
from wtforms.fields import TextField, IntegerField, HiddenField, Label
from widgets import UnfilledTextInput
import random, hashlib


class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'': return
		super(NullableIntegerField, self).process_formdata(valuelist)
		
		
class UnfilledTextField(TextField):
	widget = UnfilledTextInput()

		
class ArithmeticCaptchaField(TextField):
	widget = UnfilledTextInput()
	
	def __init__(self, first_range, second_range, **kwargs):
		super(ArithmeticCaptchaField, self).__init__(**kwargs)
		first = random.randrange(first_range[0], first_range[1])
		second = random.randrange(second_range[0], second_range[1])
		self.label = Label(self.id, '{0} + {1} ='.format(first, second))
		#self.hidden = HiddenField(default=self.generate_hash(first + second))
		self.hash = self.generate_hash(first + second)
		
		
	def process_formdata(self, valuelist):
		if valuelist:
			if self.hidden.data != self.generate_hash(self.data):
				raise ValueError(u'Ответ неверный')
		
		
	def generate_hash(self, value):
		m = hashlib.md5()
		m.update('hey{0}moo{1}se'.format(str(value), self.name))
		return m.hexdigest()