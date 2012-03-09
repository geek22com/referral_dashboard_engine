from decimal import Decimal


class FieldBase:
	def __init__(self, xpath, readonly=False, default=None):
		if not xpath:
			raise ValueError('No xpath supplied for Field')
		self.xpath = xpath
		self.readonly = readonly
		self.default = default
	
	def xpath_unique(self, xml):
		elements = xml.xpath(self.xpath)
		if elements:
			if len(elements) > 1:
				raise ValueError('More than one XPath match for non-collection field')
			else:
				return elements[0]
		return None
	
	def xpath_list(self, xml):
		return xml.xpath(self.xpath)	
	
	def process(self, xml=None, value=None):
		raise NotImplementedError()
		
	def default_value(self):
		try:
			return self.default()
		except TypeError:
			return self.default


class Field(FieldBase):
	def process(self, xml=None, value=None):
		xml_value = self.xpath_unique(xml) if xml is not None else None
		if value is not None:
			return self.process_value(value)
		elif xml_value is not None:
			return self.process_xmlvalue(xml_value)
		else:
			return self.default_value()
	
	def process_value(self, value):
		return value
	
	def process_xmlvalue(self, value):
		return value


class PrimitiveField(Field):
	value_type = None
	
	def process_value(self, value):
		if not isinstance(value, self.value_type):
			return self.value_type(value)
		return value
	
	def process_xmlvalue(self, value):
		return self.value_type(value)


class StringField(PrimitiveField):
	value_type = unicode

class IntegerField(PrimitiveField):
	value_type = int

class FloatField(PrimitiveField):
	value_type = float

class DecimalField(PrimitiveField):
	value_type = Decimal

class ModelField(PrimitiveField):
	def __init__(self, model, xpath, readonly=False, default=None):	
		PrimitiveField.__init__(self, xpath, readonly=readonly, default=default)
		if not model:
			raise ValueError('No model supplied for ModelField')
		self.value_type = model


class Collection(FieldBase):
	collection_type = None
	
	def __init__(self, field_type, xpath, default=[], **params):
		FieldBase.__init__(self, xpath=xpath, default=default, **params)
		self.field_type = field_type
		self.field_params = params
		
	def process(self, xml=None, value=None):
		xml_values = self.xpath_list(xml) if xml is not None else []
		
		if value is not None:
			return self.collection_type(self.process_item(item) for item in value)
		elif xml_values:
			field = self.field_type(xpath='.', **self.field_params)
			return self.collection_type(field.process(xml_value) for xml_value in xml_values)
		else:
			return self.default_value()
	
	def process_item(self, item):
		return item


class List(Collection):
	collection_type = list

class Set(Collection):
	collection_type = set







