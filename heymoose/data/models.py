# -*- coding: utf-8 -*-
from base import models, types, registry
from base.fields import Field, FieldList, FieldSet
from heymoose import app
import enums
import os


class IdentifiableModel(models.ModelBase):
	id = Field(types.Integer, '@id', readonly=True)
	
	def __cmp__(self, other):
		return self.id - other.id


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
	register_time = Field(types.DateTime, 'register-time')
	
	developer_account = Field('Account', 'developer-account')
	customer_account = Field('Account', 'customer-account')
	customer_secret = Field(types.String, 'customer-secret')
	
	orders = FieldList('Order', 'orders/order')
	apps = FieldList('App', 'apps/app')
	roles = FieldList(enums.Roles, 'roles/role')
	
	referrer = Field(types.Integer, 'referrer')
	referrals = FieldList(types.String, 'referrals/referral')
	revenue = Field(types.Decimal, 'revenue')
	
	stats = Field('UserStat', 'stats')
	
	@property
	def account(self): return self.developer_account or self.customer_account
	
	@property
	def active(self): return self.confirmed and not self.blocked
	
	@property
	def full_name(self): return u'{0} {1}'.format(self.first_name, self.last_name)
	
	@property
	def is_developer(self): return enums.Roles.DEVELOPER in self.roles
	@property
	def is_customer(self): return enums.Roles.CUSTOMER in self.roles
	@property
	def is_affiliate(self): return enums.Roles.AFFILIATE in self.roles
	@property
	def is_advertiser(self): return enums.Roles.ADVERTISER in self.roles
	

class Account(IdentifiableModel):
	balance = Field(types.Decimal, 'balance')

class Transaction(IdentifiableModel):
	diff = Field(types.Decimal, 'diff')
	balance = Field(types.Decimal, 'balance')
	description = Field(types.String, 'description')
	type = Field(enums.TransactionTypes, 'type')
	creation_time = Field(types.DateTime, 'creation-time')
	end_time = Field(types.DateTime, 'end-time')
	
	def type_verbose(self):
		desc = self.type.desc
		if self.type == 'WITHDRAW_DELETED':
			desc += u' ({0})'.format(self.description)
		return desc


class Order(IdentifiableModel):
	offer_id = Field(types.Integer, 'offer-id')
	type = Field(enums.OrderTypes, 'type')
	
	account = Field('Account', 'account')
	user = Field('User', 'user')
	stats = Field('OrderStat', 'stats')
	
	cpa = Field(types.Decimal, 'cpa')
	title = Field(types.String, 'title')
	url = Field(types.String, 'url')
	video_url = Field(types.String, 'video-url')
	description = Field(types.String, 'description')
	banners = Field('Banner', 'banners')
	
	auto_approve = Field(types.Boolean, 'auto-approve')
	reentrant = Field(types.Boolean, 'reentrant')
	
	male = Field(types.Boolean, 'male')
	min_age = Field(types.Integer, 'min-age')
	max_age = Field(types.Integer, 'max-age')
	min_hour = Field(types.Integer, 'min-hour')
	max_hour = Field(types.Integer, 'max-hour')
	
	city_filter_type = Field(enums.FilterTypes, 'city-filter-type')
	cities = FieldSet('City', 'cities/city')
	app_filter_type = Field(enums.FilterTypes, 'app-filter-type')
	apps = FieldSet('App', 'apps/app')
	
	disabled = Field(types.Boolean, 'disabled')
	paused = Field(types.Boolean, 'paused')
	creation_time = Field(types.DateTime, 'creation-time')
	
class OrderStat(IdentifiableModel):
	shows_overall = Field(types.Integer, 'shows-overall')
	actions_overall = Field(types.Integer, 'actions-overall')

class City(IdentifiableModel):
	name = Field(types.String, 'name')
	disabled = Field(types.Boolean, 'disabled')

class App(IdentifiableModel):
	pass

class UserStat(IdentifiableModel):
	payments = Field(types.Decimal, 'payments')
	unpaid_actions = Field(types.Integer, 'unpaid-actions')


class SubOffer(IdentifiableModel):
	parent = Field('Offer', 'parent')
	title = Field(types.String, 'title')
	auto_approve = Field(types.Boolean, 'auto-approve')
	reentrant = Field(types.Boolean, 'reentrant')
	creation_time = Field(types.DateTime, 'creation-time')
	cpa_policy = Field(enums.CpaPolicies, 'cpa-policy')
	cost = Field(types.Decimal, 'cost')
	percent = Field(types.Decimal, 'percent')
	code = Field(types.String, 'code')
	hold_days = Field(types.Integer, 'hold-days')
	
	@property
	def value(self): return self.cost or self.percent


class Offer(SubOffer):
	name = Field(types.String, 'name')
	description = Field(types.String, 'description')
	logo_filename = Field(types.String, 'logo-filename')
	url = Field(types.String, 'url')
	advertiser = Field('User', 'advertiser')
	account = Field('Account', 'account')
	pay_method = Field(enums.PayMethods, 'pay-method')
	regions = FieldList(enums.Regions, 'regions/region')
	categories = FieldList('Category', 'categories/category')
	banners = FieldList('Banner', 'banners/banner')
	approved = Field(types.Boolean, 'approved')
	active = Field(types.Boolean, 'active')
	block_reason = Field(types.String, 'block-reason')
	cookie_ttl = Field(types.Integer, 'cookie-ttl')
	
	suboffers = FieldList('SubOffer', 'suboffers/suboffer')
	grant = Field('OfferGrant', 'grant')
	
	_logos_dir = app.config.get('OFFER_LOGOS_DIR')
	
	@property
	def all_suboffers(self):
		return [self] + (self.suboffers or [])
	
	@property
	def categories_ids(self):
		return [category.id for category in self.categories]
	
	@property
	def logo(self):
		return os.path.join(self._logos_dir, self.logo_filename) if self.logo_filename else None
	
	def owned_by(self, user):
		return self.advertiser.id == user.id
	
	@property
	def visible(self):
		return self.approved and self.active


class OfferGrant(IdentifiableModel):
	offer = Field('Offer', 'offer')
	affiliate = Field('User', 'affiliate')
	back_url = Field(types.String, 'back-url')
	postback_url = Field(types.String, 'postback-url')
	message = Field(types.String, 'message')
	state = Field(enums.OfferGrantState, 'state')
	blocked = Field(types.Boolean, 'blocked')
	reject_reason = Field(types.String, 'reject-reason')
	block_reason = Field(types.String, 'block-reason')
	
	@property
	def approved(self): return not self.blocked and self.state == enums.OfferGrantState.APPROVED
	
	@property
	def rejected(self): return not self.blocked and self.state == enums.OfferGrantState.REJECTED
	
	@property
	def moderation(self): return not self.blocked and self.state == enums.OfferGrantState.MODERATION


class Banner(IdentifiableModel):
	width = Field(types.Integer, 'width')
	height = Field(types.Integer, 'height')
	mime_type = Field(types.String, 'mime-type')
	
	_mime_to_formats = {
		u'image/png': u'PNG',
		u'image/gif': u'GIF',
		u'image/jpeg': u'JPEG'
	}
	
	_banners_path = app.config.get('BACKEND_BANNERS_PATH')
	
	@property
	def size(self): return u'{0} x {1}'.format(self.width, self.height)
	
	@property
	def format(self): return self._mime_to_formats.get(self.mime_type, 'UNKNOWN')
	
	@property
	def url(self): return os.path.join(self._banners_path, str(self.id))


class Category(IdentifiableModel):
	name = Field(types.String, 'name')
	grouping = Field(types.String, 'grouping')


registry.register_models_from_module(__name__)