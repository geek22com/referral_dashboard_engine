# -*- coding: utf-8 -*-
import heymoose.core.actions.roles as roles

class MetaModel(type):
	def __new__(cls, name, bases, dct):
		attributes = dct['attributes']
		return type.__new__(cls, name, bases, dct)

	def __init__(cls, name, bases, dct):
		attributes = dct['attributes']
		if not attributes:
			return

		for attr in attributes:
			attr_name = "_" + attr
			attr_getter = lambda self, attr_name=attr_name: getattr(self, attr_name)
			setattr(cls, attr, property(fget=attr_getter))


class BaseModel(object):
	attributes = []
	__metaclass__ = MetaModel

	def __init__(self, **kwargs):
		for k, v in kwargs.iteritems():
			nm = "_" + k
			setattr(self, nm, v)


class User(BaseModel):
	attributes = ['id',
	              'email',
	              'password_hash',
	              'nickname',
	              'orders',
	              'customer_balance',
                  'customer_secret',
	              'developer_balance',
	              'apps',
	              'roles']

	def is_developer(self):
		return roles.DEVELOPER in self.roles

	def is_customer(self):
		return roles.CUSTOMER in self.roles

	def is_admin(self):
		return roles.ADMIN in self.roles

	def is_somebody(self):
		return len(self.roles) > 0

class Order(BaseModel):
	attributes = ['id',
	              'title',
	              'balance',
	              'body',
	              'cpa',
	              'approved',
	              'user_id']


class App(BaseModel):
	attributes = ['id',
	              'secret',
	              'user_id',
	              'callback',
	              'deleted',
                  'url']


class Action(BaseModel):
	attributes = ['id',
	              'performer_id',
	              'offer_id',
	              'done',
	              'deleted',
	              'creation_time']
