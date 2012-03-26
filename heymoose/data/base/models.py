from fields import FieldBase


class ModelMeta(type):
	def __init__(cls, name, bases, attrs):
		type.__init__(cls, name, bases, attrs)
		cls.fields = None
		
	def __call__(cls, *args, **kwargs): #@NoSelf
		if cls.fields is None:
			cls.fields = dict()
			for attr_name in dir(cls):
				attr_value = getattr(cls, attr_name)
				if isinstance(attr_value, FieldBase):
					cls.fields[attr_name] = attr_value
			for name, field in cls.fields.iteritems():
				setattr(cls, name, cls._property_for_field(name, field))
		return type.__call__(cls, *args, **kwargs)
			
	def _property_for_field(self, name, field):
		if not field.readonly:
			return property(lambda self: self.get_field_value(name), lambda self, v: self.set_field_value(name, v))
		else:
			return property(lambda self: self.get_field_value(name))


class ModelBase(object):
	__metaclass__ = ModelMeta
	
	def __init__(self, xml=None, **kwargs):
		self._values = dict()
		self._dirty = dict()
		self._parse(xml, **kwargs)
	
	def get_field_value(self, name):
		self._check_field_exists(name)
		return self._values[name]
	
	def set_field_value(self, name, value):
		self._check_field_exists(name)
		if self._values[name] != value:
			self.mark_dirty(name)
			self._values[name] = value
	
	def is_dirty(self, name):
		return (name in self._dirty)
			
	def mark_dirty(self, name, force=False):
		if not self.is_dirty(name) or force:
			self._dirty[name] = self._values[name]
	
	def _check_field_exists(self, name):
		if name not in self.fields:
			raise KeyError('No field with name {0}'.format(name))
	
	def _parse(self, xml, **kwargs):
		for name, field in self.fields.iteritems():
			self._values[name] = kwargs.get(name, None) or field.parse(xml)
	
	def updated(self):
		return len(self._dirty.keys()) > 0
	
	def updated_values(self):
		return dict((name, self._values[name]) for name in self._dirty.iterkeys())
	
	def values(self):
		return self._values