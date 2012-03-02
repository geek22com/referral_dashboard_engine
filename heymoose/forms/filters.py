# -*- coding: utf-8 -*-
from heymoose import app

@app.template_filter('formfield')
def formfield(field, **kwargs):
	'''Helper filter for field macro'''
	css_class = kwargs.pop('class', '') or kwargs.pop('class_', '')
	attrs = dict()
	
	for validator in field.validators:
		if hasattr(validator, 'css_class') and validator.css_class:
			css_class += ' ' + validator.css_class
		if hasattr(validator, 'data_attrs'):
			attrs.update(validator.data_attrs())
	
	attrs.update({'class': css_class, 'class_': css_class})
	attrs.update(kwargs)
	return field(**attrs)

@app.template_filter('fieldlist')
def fieldlist(values):
	'''Helper filter for multifield_desc macro'''
	return [value[0] for value in values if not isinstance(value, str) and not isinstance(value, unicode)]