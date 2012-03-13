from types import TypeBase, ModelType, LazyModelType
import models

class FieldBase(object):
	def __init__(self, field_type_class, xpath, readonly=False, **params):
		if not field_type_class:
			raise ValueError('No type supplied for {0}'.format(self.__class__.__name__))
		if not xpath:
			raise ValueError('No xpath supplied for {0}'.format(self.__class__.__name__))
		self.field_type = self.init_field_type(field_type_class, **params)
		self.xpath = xpath
		self.readonly = readonly
		self.params = params
	
	def xpath_unique(self, xml):
		elements = xml.xpath(self.xpath)
		if elements:
			if len(elements) > 1:
				raise ValueError('Expected unique value but there is more than one XPath match')
			else:
				return elements[0]
		return None
	
	def xpath_list(self, xml):
		return xml.xpath(self.xpath)
	
	def parse(self, xml):
		raise NotImplementedError()
	
	def validate(self, value):
		raise NotImplementedError()
	
	def init_field_type(self, field_type_class, **params):
		if isinstance(field_type_class, str):
			return LazyModelType(field_type_class, **params)
		elif issubclass(field_type_class, models.ModelBase):
			return ModelType(field_type_class, **params)
		elif issubclass(field_type_class, TypeBase):
			return field_type_class(**params)
		else:
			raise TypeError(u'Field type must be subclass of TypeBase, ModelBase or model name')


class Field(FieldBase):
	def parse(self, xml):
		matched_xml = self.xpath_unique(xml) if xml is not None else None
		if matched_xml is not None:
			return self.field_type.parse(matched_xml)
		else:
			return self.field_type.default_value()


class FieldCollection(FieldBase):
	collection_class = None
	
	def parse(self, xml):
		matched_xml_list = self.xpath_list(xml) if xml is not None else []
		if matched_xml_list:
			return self.collection_class([self.field_type.parse(matched_xml) for matched_xml in matched_xml_list])
		else:
			return [] #self.field_type.default_value()

class FieldList(FieldCollection):
	collection_class = list

class FieldSet(FieldCollection):
	collection_class = set







