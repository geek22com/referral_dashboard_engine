import registry

class TypeBase(object):
	def __init__(self, default=None):
		self.default = default
	
	def validate(self, value):
		raise NotImplementedError()
	
	def parse(self, xml):
		raise NotImplementedError()
	
	def default_value(self):
		try:
			return self.default()
		except TypeError:
			return self.default


class PrimitiveType(TypeBase):
	type_class = None
	
	def validate(self, value):
		if not isinstance(value, self.type_class):
			raise ValueError(u'Invalid value {0} for field type {1}'.format(value, self.__class__.__name__))
	
	def parse(self, xml):
		if hasattr(xml, 'text'):
			return self.type_class(xml.text)
		return self.type_class(xml)


class String(PrimitiveType):
	type_class = unicode
	
	def __init__(self, min=None, max=None, default=None):
		super(String, self).__init__(default)
		self.min = min
		self.max = max
		
	def validate(self, value):
		if self.min is not None and len(value) < self.min:
			raise ValueError(u'Too short string')
		if self.max is not None and len(value) > self.max:
			raise ValueError(u'Too long string')


class DecimalBase(PrimitiveType):
	def __init__(self, min=None, max=None, default=None):
		super(DecimalBase, self).__init__(default)
		self.min = min
		self.max = max
	
	def validate(self, value):
		if self.min is not None and value < self.min:
			raise ValueError(u'Value must be greater or equal than {0}'.format(self.min))
		if self.max is not None and value > self.max:
			raise ValueError(u'Value must be less or equal than {0}'.format(self.max))


class Integer(DecimalBase):
	type_class = int


class ModelType(TypeBase):
	def __init__(self, model_class, default=None):
		super(ModelType, self).__init__(default)
		self.model_class = model_class
	
	def validate(self, value):
		if not isinstance(value, self.model_class):
			raise ValueError(u'Invalid value {0} for field with model type {1}'
				.format(value, self.model_class.__class__.__name__))
	
	def parse(self, xml):
		return self.model_class(xml)


class LazyModelType(ModelType):
	def __init__(self, model_name, default=None):
		super(LazyModelType, self).__init__(None, default=default)
		self.model_name = model_name
	
	@property
	def model_class(self):
		if getattr(self, '_model_class', None) is None:
			self._model_class = registry.get_model(self.model_name)
		return self._model_class
	
	@model_class.setter
	def model_class(self, value):
		self._model_class = value
