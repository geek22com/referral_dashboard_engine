from base import models, fields

class IdentifiableModel(models.Model):
	id = fields.IntegerField('@id', readonly=True)

class User(IdentifiableModel):
	email = fields.StringField('email')