# -*- coding: utf-8 -*-
from base import models, types, registry
from base.fields import Field, FieldList

class IdentifiableModel(models.ModelBase):
	id = Field(types.Integer, '@id', readonly=True)

class User(IdentifiableModel):
	email = Field(types.String, 'email')
	password_hash = Field(types.String, 'password-hash')
	first_name = Field(types.String, 'first-name')
	last_name = Field(types.String, 'last-name')
	organization = Field(types.String, 'organization')
	phone = Field(types.String, 'phone')
	source_url = Field(types.String, 'source-url')
	messenger_type = Field(types.String, 'messenger-type')
	messenger_uid = Field(types.String, 'messenger-uid')
	
	confirmed = Field(types.Boolean, 'confirmed')
	blocked = Field(types.Boolean, 'blocked')
	
	roles = FieldList(types.String, 'roles/role')
	developer_account = Field('Account', 'developer-account')
	customer_account = Field('Account', 'customer-account')
	orders = FieldList('Order', 'orders/order')
	
	@property
	def account(self):
		return self.developer_account or self.customer_account

class Account(IdentifiableModel):
	balance = Field(types.Decimal, 'balance')
	
class Order(IdentifiableModel):
	title = Field(types.String, 'title', default=u'UNKNOWN')
	user = Field('User', 'user')


registry.register_models_from_module(__name__)