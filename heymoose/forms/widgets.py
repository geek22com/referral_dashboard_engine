from wtforms.widgets import TextInput, CheckboxInput, ListWidget #@UnusedImport

class UnfilledTextInput(TextInput):
	'''
	Acts like TextInput, but this field will not reproduce the value on a form
	submit by default. To have the value filled in, set `hide_value` to
	`False`.
	'''
	def __init__(self, hide_value=True):
		self.hide_value = hide_value
	
	def __call__(self, field, **kwargs): 
		if self.hide_value:
			kwargs['value'] = ''
		return super(UnfilledTextInput, self).__call__(field, **kwargs)