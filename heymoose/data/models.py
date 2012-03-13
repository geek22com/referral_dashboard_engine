# -*- coding: utf-8 -*-
from heymoose import resource
from base import models, types, registry
from base.fields import Field, FieldList
from functools import partial

class ResourceModel(models.ModelBase):
	resource = None
	
	def __getattr__(self, name):
		'''Some proxying: Model.resource.foo(obj) == obj.foo()'''
		if self.resource is not None and hasattr(self.resource, name):
			return partial(getattr(self.resource, name), self)
		raise AttributeError(name)


class IdentifiableModel(ResourceModel):
	id = Field(types.Integer, '@id', readonly=True)
	
	def save(self):
		if self.id is None:
			self._values['id'] = self.resource.add(self)
		else:
			self.resource.update(self)
	
	def __cmp__(self, other):
		return self.id - other.id


class User(IdentifiableModel):
	resource = resource.UserResource()
	
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
	register_time = Field(types.DateTime, 'register-time')
	
	developer_account = Field('Account', 'developer-account')
	customer_account = Field('Account', 'customer-account')
	customer_secret = Field(types.String, 'customer-secret')
	
	orders = FieldList('Order', 'orders/order')
	apps = FieldList('App', 'apps/app')
	roles = FieldList(types.String, 'roles/role')
	
	referrer = Field(types.Integer, 'referrer')
	referrals = FieldList(types.String, 'referrals/referral')
	revenue = Field(types.Decimal, 'revenue')
	
	stats = Field('UserStat', 'stats')
	
	@property
	def account(self):
		return self.developer_account or self.customer_account

class Account(IdentifiableModel):
	balance = Field(types.Decimal, 'balance')
	
class Order(IdentifiableModel):
	title = Field(types.String, 'title', default=u'UNKNOWN')
	user = Field('User', 'user')

class App(IdentifiableModel):
	pass

class UserStat(IdentifiableModel):
	payments = Field(types.Decimal, 'payments')
	unpaid_actions = Field(types.Integer, 'unpaid-actions')
	
	
registry.register_models_from_module(__name__)