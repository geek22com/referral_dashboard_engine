# -*- coding: utf-8 -*-
from wtforms.fields import TextField, IntegerField, FileField
from PIL import Image
from widgets import UnfilledTextInput


class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'': return
		super(NullableIntegerField, self).process_formdata(valuelist)
		
		
class UnfilledTextField(TextField):
	widget = UnfilledTextInput()
	
	
class ImageField(FileField):
	def process_formdata(self, valuelist):
		if valuelist:
			try:
				self.data = Image.open(valuelist[0])
				valuelist[0].seek(0)
			except:
				raise ValueError(u'Файл не является изображением')
			