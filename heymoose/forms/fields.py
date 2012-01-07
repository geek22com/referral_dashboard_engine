# -*- coding: utf-8 -*-
from wtforms.fields import TextField, IntegerField, FileField
from PIL import Image
from heymoose.utils import swfheader
from widgets import UnfilledTextInput


class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'':
			self.data = None
			return
		super(NullableIntegerField, self).process_formdata(valuelist)
		
		
class UnfilledTextField(TextField):
	widget = UnfilledTextInput()
	
	
class ImageField(FileField):
	def process_formdata(self, valuelist):
		if valuelist and valuelist[0].filename != '':
			try:
				self.data = Image.open(valuelist[0])
				self.width = self.data.size[0]
				self.height = self.data.size[1]
				self.format = self.data.format.lower()
			except:
				raise ValueError(u'Файл не является изображением')
			finally:
				valuelist[0].seek(0)
		else:
			self.data = None
			
			
class BannerField(FileField):
	def process_formdata(self, valuelist):
		if valuelist and valuelist[0].filename != '':
			success = False
			try:
				self.data = Image.open(valuelist[0])
				self.width = self.data.size[0]
				self.height = self.data.size[1]
				self.format = self.data.format.lower()
				if self.format not in ('jpg', 'jpeg'):
					self.mime_type = 'image/{0}'.format(self.format)
				else:
					self.mime_type = 'image/jpeg'
				success = True
			except:
				pass
			finally:
				valuelist[0].seek(0)
			if success: return
			
			try:
				self.data = swfheader.parse(valuelist[0])
				self.width = self.data['width']
				self.height = self.data['height']
				self.format = 'swf'
				self.mime_type = 'application/x-shockwave-flash'
				success = True
			except:
				pass
			finally:
				valuelist[0].seek(0)
			if success: return
			
			raise ValueError(u'Формат файла не подходит для отображения в виде баннера')
		else:
			self.data = None





