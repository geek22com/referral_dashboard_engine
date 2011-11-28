from wtforms.fields import IntegerField

class NullableIntegerField(IntegerField):
	def process_formdata(self, valuelist):
		value = valuelist[0]
		if value is None or value == '' or value == u'': return
		super(NullableIntegerField, self).process_formdata(valuelist)