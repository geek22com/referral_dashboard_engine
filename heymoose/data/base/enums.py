from operator import attrgetter

class EnumMeta(type):
	def __new__(cls, name, bases, attrs):
		bases_elements = []
		if bases and bases[0].__name__ not in ('object', 'Enum'):
			bases_elements += bases[0].elements
		elements = [value for value in attrs.values() if value.__class__.__name__ == 'EnumElement']
		attrs['elements'] = bases_elements + sorted(elements, key=attrgetter('creation_counter'))
		return super(EnumMeta, cls).__new__(cls, name, bases, attrs)


class Enum(object):
	__metaclass__ = EnumMeta
	count = 0
	
	def __init__(self):
		raise TypeError('Enum initialization is forbidden')
	
	def __new__(self, *args, **kwargs):
		raise TypeError('Enum initialization is forbidden')
	
	@classmethod
	def values(cls, attr=None):
		if attr is None:
			return cls.elements
		else:
			return [getattr(element, attr) for element in cls.elements]
	
	@classmethod
	def tuples(cls, *attrs):
		return [(element, ) + tuple(getattr(element, attr) for attr in attrs) for element in cls.elements]
	
	@classmethod
	def has(cls, value):
		return (value in cls.elements)
	
	@classmethod
	def of(cls, value):
		return cls.elements[cls.elements.index(value)]
			

def e(val, **kwargs):
	elem_type = type(val)
	class EnumElement(elem_type):
		def __new__(cls, value, **kwargs):
			obj = elem_type.__new__(cls, value)
			obj.creation_counter = Enum.count
			Enum.count += 1
			for attr, attrval in kwargs.iteritems():
				setattr(obj, attr, attrval)
			return obj
	return EnumElement(val, **kwargs)