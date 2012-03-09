from fields import FieldBase
from lxml import etree

class ModelMeta:
	def __init__(self, name, bases, attrs):
		self.fields = dict((name, field) for name, field in attrs.iteritems() if isinstance(field, FieldBase))
		for name, field in self.fields.iteritems():
			setattr(self, name, self._property_for_field(name, field))
			
	def _property_for_field(self, name, field):
		if not field.readonly:
			return property(lambda self: self.get_field_value(name), lambda self, v: self.set_field_value(name, v))
		else:
			return property(lambda self: self.get_field_value(name))


class Model:
	__metaclass__ = ModelMeta
	
	def __init__(self, xml=None, **kwargs):
		self._values = dict()
		self._dirty = dict()
		self._process(xml, **kwargs)
	
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
	
	def _process(self, xml, **kwargs):
		if xml is not None and (isinstance(xml, str) or isinstance(xml, unicode)):
			xml = etree.fromstring(xml)
		for name, field in self.fields.iteritems():
			self._values[name] = field.process(xml, kwargs[name])