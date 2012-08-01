from flask import current_app


def config_value(name, default=None):
	return current_app.config.get(name, default)


def config_accessor(name, default=None):
	return lambda: config_value(name, default)


class ConfigAttribute(object):
	'''Makes an attribute forward to the config'''
	
	def __init__(self, name, default=None):
		self.__name__ = name
		self.default = default

	def __get__(self, obj, type=None):
		if obj is None: return self
		return current_app.config.get(self.__name__, self.default)

	def __set__(self, obj, value):
		current_app.config[self.__name__] = value
