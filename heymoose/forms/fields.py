# -*- coding: utf-8 -*-
from wtforms.fields import TextField, IntegerField, DecimalField, FileField, SelectField, SelectMultipleField
from PIL import Image
from heymoose import resource as rc
from heymoose.utils import swfheader, svgheader
from heymoose.data import enums
import widgets


class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'':
			self.data = None
			return
		super(NullableIntegerField, self).process_formdata(valuelist)

class NullableDecimalField(DecimalField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'':
			self.data = None
			return
		super(NullableDecimalField, self).process_formdata(valuelist)
		
class NullableTextField(TextField):
	def process_formdata(self, valuelist):
		super(NullableTextField, self).process_formdata(valuelist)
		self.data = self.data or None
		
class NullableSelectField(SelectField):
	def post_validate(self, form, validation_stopped):
		super(NullableSelectField, self).post_validate(form, validation_stopped)
		self.data = self.data or None
		
		
class UnfilledTextField(TextField):
	widget = widgets.UnfilledTextInput()
	
	
class ImageField(FileField):
	def process_formdata(self, valuelist):
		if valuelist and valuelist[0].filename != '':
			try:
				self.data = Image.open(valuelist[0])
				self.width = self.data.size[0]
				self.height = self.data.size[1]
				self.format = self.data.format.lower()
				if self.format not in ('jpg', 'jpeg'):
					self.mime_type = 'image/{0}'.format(self.format)
				else:
					self.mime_type = 'image/jpeg'
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
			
			try:
				self.data = svgheader.parse(valuelist[0])
				self.width = self.data['width']
				self.height = self.data['height']
				self.format = 'svg'
				self.mime_type = 'image/svg+xml'
				success = True
			except:
				pass
			finally:
				valuelist[0].seek(0)
			if success: return
			
			raise ValueError(u'Формат файла не подходит для отображения в виде баннера')
		else:
			self.data = None


class CheckboxListField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()


class CategorizedCheckboxListField(CheckboxListField):
	class _CategorizedCheckboxInput(widgets.CheckboxInput):
		def __init__(self, input_type=None, category=u''):
			super(CategorizedCheckboxListField._CategorizedCheckboxInput, self).__init__(input_type)
			self.category = category
			
		def __call__(self, field, **kwargs):
			kwargs.update({'data-category': self.category})
			return super(CategorizedCheckboxListField._CategorizedCheckboxInput, self).__call__(field, **kwargs)
	
	def iter_choices(self):
		for value, label, category in self.choices:
			if self.data is not None:
				selected = self.coerce(value) in self.data
			else:
				selected = self.default or False
			yield (value, label, category, selected)
	
	def __iter__(self):
		opts = dict(_name=self.name, _form=None)
		for i, (value, label, category, checked) in enumerate(self.iter_choices()):
			opt = self._Option(widget=self._CategorizedCheckboxInput(category=category),
							label=label, id=u'%s-%d' % (self.id, i), **opts)
			opt.process(None, value)
			opt.checked = checked
			yield opt


class RegionsField(CheckboxListField):
	def __init__(self, label=None, validators=None, **kwargs):
		super(RegionsField, self).__init__(label, validators, choices=enums.Regions.tuples('name'), **kwargs)
	
	def populate_obj(self, obj, name):
		setattr(obj, name, set(self.data))


class CategoriesField(CategorizedCheckboxListField):
	def __init__(self, label=None, validators=None, **kwargs):
		self.categories = [cat for cat in rc.categories.list() if cat.name]
		choices = [(c.id, c.name, c.grouping) for c in self.categories]
		super(CategoriesField, self).__init__(label, validators, int, choices, **kwargs)
	
	def process_formdata(self, valuelist):
		super(CategoriesField, self).process_formdata(valuelist)
		categories_dict = {category.id : category for category in self.categories}
		self.selected_categories = []
		if self.data:
			for id in self.data:
				if id in categories_dict:
					self.selected_categories.append(categories_dict.get(id))
		self.selected_categories = set(self.selected_categories)
	
	def process_data(self, value):
		try:
			self.data = [category.id for category in value]
		except (ValueError, TypeError):
			self.data = None
	
	def populate_obj(self, obj, name):
		setattr(obj, name, self.selected_categories)


class OfferField(SelectField):
	def set_offers(self, offers, empty=(0, u'(все)')):
		choices = [(offer.id, offer.name) for offer in offers]
		if empty: choices.insert(0, empty)
		self.choices = choices
	'''
	def process_formdata(self, valuelist):
		super(OfferField, self).process_formdata(valuelist)
		self.data = int(self.data) if self.data else None
	
	def pre_validate(self, form):
		print 'DADADAD', self.data
		if not self.data: self.data = u''
		super(OfferField, self).pre_validate(form)'''
