from fields import FieldBase
from lxml import etree

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
		if name not in self._dirty:
			self._dirty[name] = self._values[name]
		self._values[name] = value
	
	def _check_field_exists(self, name):
		if name not in self.fields:
			raise KeyError('No field with name {0}'.format(name))
	
	def _parse(self, xml, **kwargs):
		if xml is not None and (isinstance(xml, str) or isinstance(xml, unicode)):
			xml = etree.fromstring(xml)
		for name, field in self.fields.iteritems():
			self._values[name] = kwargs.get(name, None) or field.parse(xml)