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
	
	
class OrderTypes:
	ALL = ('REGULAR', 'BANNER', 'VIDEO')
	REGULAR, BANNER, VIDEO = ALL
	
	_verbose = dict(
		REGULAR=u'Обычный',
		BANNER=u'Баннер',
		VIDEO=u'Видео'
	)
	
	def verbose(self, type):
		return self._verbose.get(type, None)
	

class Order(BaseModel):
	attributes = ['id',
				  'balance',
				  'user',
				  'user_id',
				  'cpa',
	              'disabled',
	              'creation_time',
	              'offer_id',
	              'title',
	              'url',
	              'type',
	              'video_url',
	              'description',
	              'image',
	              'banners',
	              'auto_approve',
	              'reentrant',
	              'allow_negative_balance',
	              'male',
	              'min_age',
	              'max_age',
	              'city_filter_type',
	              'cities']
	
	def is_regular(self): return self.type == OrderTypes.REGULAR
	def is_banner(self): return self.type == OrderTypes.BANNER
	def is_video(self):	return self.type == OrderTypes.VIDEO


class BannerSize(BaseModel):
	attributes = ['id', 'width', 'height']
	
	
class Banner(BaseModel):
	attributes = ['id', 'size', 'image']


class City(BaseModel):
	attributes = ['id', 'name']


class App(BaseModel):
	attributes = ['id',
				  'title',
	              'secret',
	              'user_id',
	              'user',
	              'platform',
	              'callback',
	              'deleted',
                  'url',
                  'creation_time']


class Action(BaseModel):
	attributes = ['id',
	              'performer_id',
	              'performer',
	              'offer_id',
	              'order',
	              'app',
	              'done',
	              'deleted',
	              'creation_time',
	              'approve_time',
	              'attempts']
	
	
class Performer(BaseModel):
	attributes = ['id',
				  'ext_id',
				  'platform',
				  'creation_time',
				  'inviter',
				  'male',
				  'year']
	
	
class OrderShow(BaseModel):
	attributes = ['id',
				  'show_time']
