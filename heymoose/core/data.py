# -*- coding: utf-8 -*-
import sys

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
	              'developer_balance',
	              'apps',
	              'roles']


class Order(BaseModel):
	attributes = ['id',
	              'title',
	              'balance',
	              'body',
	              'cpa',
	              'user_id']


class App(BaseModel):
	attributes = ['id',
	              'secret',
	              'user_id']


class Action(BaseModel):
	attributes = ['id',
	              'performer_id',
	              'offer_id',
	              'done',
	              'deleted',
	              'creation_time']
