# -*- coding: utf-8 -*-
from heymoose import app
from heymoose.utils import gen
import heymoose.core.actions.roles as roles
import os, mimetypes, base64, hashlib

class MetaModel(type):
	def __new__(cls, name, bases, dct):
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
	              'first_name',
	              'last_name',
	              'organization',
	              'phone',
	              'source_url',
	              'messenger_type',
	              'messenger_uid',
	              'confirmed',
	              'blocked',
	              'register_time',
	              'orders',
                  'customer_secret',
	              'customer_account',
	              'developer_account',
	              'apps',
	              'roles',
	              'referrer',
	              'referrals',
	              'revenue',
	              'stats']

	def is_developer(self): return roles.DEVELOPER in self.roles
	def is_customer(self): return roles.CUSTOMER in self.roles
	def is_admin(self): return roles.ADMIN in self.roles
	def is_advertiser(self): return roles.ADVERTISER in self.roles
	def is_affiliate(self): return roles.AFFILIATE in self.roles
	def is_somebody(self): return len(self.roles) > 0
	
	def full_name(self):
		return u'{0} {1}'.format(self.first_name, self.last_name)
	
	def get_refcode(self):
		key = app.config.get('REFERRAL_CRYPT_KEY', 'qwertyui12345678')
		salt = 'hmrefsalt'
		data = '{0}${1}'.format(self.id, salt)
		data = '{0:X<16}'.format(data)
		return gen.aes_base16_encrypt(key, data).lower()
	
	def get_confirm_code(self):
		m = hashlib.md5()
		m.update('hey{0}moose{1}confirm'.format(self.id, self.email))
		return m.hexdigest()
	
	def check_confirm_code(self, code):
		return code == self.get_confirm_code()


class UserStat(BaseModel):
	attributes = ['id', 'payments', 'unpaid_actions']

	
class Account(BaseModel):
	attributes = ['id', 'balance', 'allow_negative_balance']
	
	
class Transaction(BaseModel):
	attributes = ['id',
				  'diff',
				  'balance',
				  'description',
				  'type',
				  'creation_time',
				  'end_time']
	
	types = {
		'UNKNOWN' 					: u'--',
		'TRANSFER' 					: u'Перевод',
		'RESERVATION' 				: u'Резервирование',
		'ACTION_APPROVED' 			: u'Оплата за клики',
		'MLM' 						: u'MLM',
		'RESERVATION_CANCELLED'		: u'Отмена резервирования',
		'REPLENISHMENT_ROBOKASSA'	: u'Пополнение счета с помощью системы "RoboKassa"',
		'WITHDRAW' 					: u'Выплата разработчику',
		'REPLENISHMENT_ADMIN'		: u'Пополнение счета администрацией',
		'WITHDRAW_DELETED'			: u'Отмена выплаты разработчику'
	}
	
	def type_verbose(self):
		t = self.types.get(self.type, u'')
		if self.type == 'WITHDRAW_DELETED':
			t += u' ({0})'.format(self.description)
		return t
	

class Withdrawal(BaseModel):
	attributes = ['id', 'amount', 'timestamp', 'done']

	
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
				  'account',
				  'user',
				  'user_id',
				  'cpa',
	              'disabled',
	              'paused',
	              'creation_time',
	              'offer_id',
	              'title',
	              'url',
	              'type',
	              'stats',
	              'video_url',
	              'description',
	              'image',
	              'banners',
	              'auto_approve',
	              'reentrant',
	              'male',
	              'min_age',
	              'max_age',
	              'min_hour',
	              'max_hour',
	              'city_filter_type',
	              'cities',
	              'app_filter_type',
	              'apps']
	
	def is_regular(self): return self.type == OrderTypes.REGULAR
	def is_banner(self): return self.type == OrderTypes.BANNER
	def is_video(self):	return self.type == OrderTypes.VIDEO


class OrderStat(BaseModel):
	attributes = ['id', 'shows_overall', 'actions_overall']


class BannerSize(BaseModel):
	attributes = ['id', 'width', 'height', 'disabled']
	
	
class Banner(BaseModel):
	attributes = ['id', 'size', 'mime_type', 'image']
	
	def image_file(self):
		format = mimetypes.guess_extension(self.mime_type)
		uploaded_filename = os.path.join('banners', '{0}{1}'.format(self.id, format))
		filepath = os.path.join(app.config.get('UPLOAD_PATH'), uploaded_filename)
		if not os.path.exists(filepath):
			print 'Saving file...', uploaded_filename
			with open(filepath, 'w') as file: file.write(base64.decodestring(self.image))
		return uploaded_filename


class City(BaseModel):
	attributes = ['id', 'name', 'disabled']


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
                  'creation_time',
                  'd', 't',
                  'stats']


class AppStat(BaseModel):
	attributes = ['id', 'shows_overall', 'actions_overall', 'dau_average',
				  'dau_day0', 'dau_day1', 'dau_day2', 'dau_day3', 'dau_day4', 'dau_day5', 'dau_day6']


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
				  'year',
				  'city']
	
	def link(self):
		if self.platform == 'VKONTAKTE':
			return 'http://vkontakte.ru/id{0}'.format(self.ext_id)
		return ''
	
	
class OrderShow(BaseModel):
	attributes = ['id',
				  'show_time']
	
	
class StatCtr(BaseModel):
	attributes = ['id', 'gender', 'year', 'city', 'time', 'shows', 'actions', 'performers', 'ctr']


class Settings(BaseModel):
	attributes = ['q', 'm', 'c_min']
	c_floor = app.config.get('MIN_CPC')
	
	def c_min_safe(self): return max(self.c_floor, self.c_min)
	def c_rec(self): return round(self.c_min_safe() * self.q, 2)




