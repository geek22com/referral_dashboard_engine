from wtforms.fields import IntegerField, Label
from widgets import UnfilledTextInput
from heymoose.db.actions import captcha
import random


class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'': return
		super(NullableIntegerField, self).process_formdata(valuelist)

		
class ArithmeticCaptchaField(IntegerField):
	widget = UnfilledTextInput()
	
	def __init__(self, first_range, second_range, **kwargs):
		super(ArithmeticCaptchaField, self).__init__(**kwargs)
		first = random.randrange(first_range[0], first_range[1])
		second = random.randrange(second_range[0], second_range[1])
		self.label = Label(self.id, '{0} + {1} ='.format(first, second))
		