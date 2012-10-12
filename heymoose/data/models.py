# -*- coding: utf-8 -*-
from base import models, types, registry
from base.fields import Field, FieldList, FieldSet
from heymoose import app
from heymoose.utils.gen import generate_password_hash, aes_base16_encrypt, aes_base16_decrypt
from repos import regions_repo
from datetime import datetime
import enums
import os, hashlib, uuid


class IdentifiableModel(models.ModelBase):
	id = Field(types.Integer, '@id', readonly=True)
	
	def __cmp__(self, other):
		return self.id - other.id
	
	def __hash__(self):
		return hash(self.id)


class User(IdentifiableModel):
	email = Field(types.String, 'email')
	password_hash = Field(types.String, 'password-hash')
	first_name = Field(types.String, 'first-name')
	last_name = Field(types.String, 'last-name')
	organization = Field(types.String, 'organization')
	phone = Field(types.String, 'phone')
	source = Field(types.String, 'source')
	messenger_type = Field(types.String, 'messenger-type')
	messenger_uid = Field(types.String, 'messenger-uid')
	wmr = Field(types.String, 'wmr')
	
	confirmed = Field(types.Boolean, 'confirmed')
	blocked = Field(types.Boolean, 'blocked')
	block_reason = Field(types.String, 'block-reason')
	register_time = Field(types.DateTime, 'register-time')
	
	affiliate_account = Field('Account', 'affiliate-account')
	affiliate_account_not_confirmed = Field('Account', 'affiliate-account-not-confirmed')
	advertiser_account = Field('Account', 'advertiser-account')
	
	roles = FieldList(enums.Roles, 'roles/role')
	referrer = Field(types.Integer, 'referrer')
	referrals = FieldList(types.String, 'referrals/referral')
	revenue = Field(types.Decimal, 'revenue')
	secret_key = Field(types.String, 'secret-key')
	
	_ref_crypt_key = app.config.get('REFERRAL_CRYPT_KEY', 'qwertyui12345678')
	
	@property
	def account(self): return self.affiliate_account or self.advertiser_account
	
	@property
	def active(self): return self.confirmed and not self.blocked
	
	@property
	def full_name(self):
		if self.first_name and self.last_name:
			return u'{0} {1}'.format(self.first_name, self.last_name)
		elif self.first_name:
			return self.first_name
		elif self.last_name:
			return self.last_name
		else:
			return None
	
	@property
	def is_affiliate(self): return enums.Roles.AFFILIATE in self.roles
	@property
	def is_advertiser(self): return enums.Roles.ADVERTISER in self.roles
	@property
	def is_admin(self): return enums.Roles.ADMIN in self.roles
	
	def get_confirm_code(self):
		m = hashlib.md5()
		m.update('hey{0}moose{1}confirm'.format(self.id, self.email))
		return m.hexdigest()
	
	def check_confirm_code(self, code):
		return code == self.get_confirm_code()
	
	def get_refcode(self):
		key = app.config.get('REFERRAL_CRYPT_KEY', 'qwertyui12345678')
		salt = 'hmrefsalt'
		data = '{0}${1}'.format(self.id, salt)
		data = '{0:X<16}'.format(data)
		return aes_base16_encrypt(key, data).lower()
	
	@staticmethod
	def get_referrer_id(ref):
		try:
			id, _salt = aes_base16_decrypt(User._ref_crypt_key, ref).split('$')
			return id
		except:
			return None

	def change_password(self, raw_password):
		self.password_hash = generate_password_hash(raw_password)
	
	def generate_password(self):
		new_password = unicode(uuid.uuid4())[:8]
		self.change_password(new_password)
		return new_password


class Account(IdentifiableModel):
	balance = Field(types.Decimal, 'balance')


class AccountingEntry(IdentifiableModel):
	amount = Field(types.Decimal, 'amount')
	event = Field(enums.AccountingEvents, 'event')
	creation_time = Field(types.DateTime, 'creation-time')


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


class SubOffer(IdentifiableModel):
	parent = Field('Offer', 'parent')
	title = Field(types.String, 'title')
	auto_approve = Field(types.Boolean, 'auto-approve')
	reentrant = Field(types.Boolean, 'reentrant')
	creation_time = Field(types.DateTime, 'creation-time')
	pay_method = Field(enums.PayMethods, 'pay-method')
	cpa_policy = Field(enums.CpaPolicies, 'cpa-policy')
	cost = Field(types.Decimal, 'cost')
	cost2 = Field(types.Decimal, 'cost2')
	percent = Field(types.Decimal, 'percent')
	affiliate_cost = Field(types.Decimal, 'affiliate-cost')
	affiliate_cost2 = Field(types.Decimal, 'affiliate-cost2')
	affiliate_percent = Field(types.Decimal, 'affiliate-percent')
	code = Field(types.String, 'code')
	hold_days = Field(types.Integer, 'hold-days')
	active = Field(types.Boolean, 'active')
	exclusive = Field(types.Boolean, 'exclusive')
	
	def value(self, affiliate=False, short=False):
		if affiliate:
			cost, cost2, percent = self.affiliate_cost, self.affiliate_cost2, self.affiliate_percent
		else:
			cost, cost2, percent = self.cost, self.cost2, self.percent
		if self.pay_method == enums.PayMethods.CPC:
			return u'{0} руб.{1}'.format(cost, u' за клик' if not short else u'')
		elif self.cpa_policy == enums.CpaPolicies.FIXED:
			return u'{0} руб.{1}'.format(cost, u' за действие' if not short else u'')
		elif self.cpa_policy == enums.CpaPolicies.DOUBLE_FIXED:
			return u'{0} руб.{1} и {2} руб.{3}'.format(
				cost, u' за первое действие' if not short else u'',
				cost2, u' за последующие' if not short else u'')
		elif self.cpa_policy == enums.CpaPolicies.PERCENT:
			return u'{0}%{1}'.format(percent, u' с заказа или покупки' if not short else u'')
		return u'неизвестно'
	
	@property
	def payment_type(self):
		if self.pay_method == enums.PayMethods.CPC:
			return u'фиксированная за клик'
		elif self.cpa_policy == enums.CpaPolicies.FIXED:
			return u'фиксированная за действие'
		elif self.cpa_policy == enums.CpaPolicies.DOUBLE_FIXED:
			return u'фиксированная за первое и последующие действия'
		elif self.cpa_policy == enums.CpaPolicies.PERCENT:
			return u'процент с заказа или покупки'
		return u'неизвестно'


class Offer(SubOffer):
	name = Field(types.String, 'name')
	description = Field(types.String, 'description')
	short_description = Field(types.String, 'short-description')
	cr = Field(types.Decimal, 'cr')
	showcase = Field(types.Boolean, 'showcase')
	logo_filename = Field(types.String, 'logo-filename')
	url = Field(types.String, 'url')
	site_url = Field(types.String, 'site-url')
	advertiser = Field('User', 'advertiser')
	account = Field('Account', 'account')
	regions = FieldSet(types.String, 'regions/region')
	categories = FieldSet('Category', 'categories/category')
	banners = FieldList('Banner', 'banners/banner')
	approved = Field(types.Boolean, 'approved')
	block_reason = Field(types.String, 'block-reason')
	cookie_ttl = Field(types.Integer, 'cookie-ttl')
	token_param_name = Field(types.String, 'token-param-name')
	launch_time = Field(types.DateTime, 'launch-time')
	allow_deeplink = Field(types.Boolean, 'allow-deeplink')
	
	suboffers = FieldList('SubOffer', 'suboffers/suboffer')
	grant = Field('OfferGrant', 'grant')
	
	_logos_dir = app.config.get('OFFER_LOGOS_DIR')
	_women_categories_ids = app.config.get('WOMEN_CATEGORIES')
	_women_categories_css = ['wedding', 'pregnant', 'one_year', 'children', 'woman']
	
	@property
	def all_suboffers(self):
		return [self] + (self.suboffers or [])
	
	@property
	def active_suboffers(self):
		return [s for s in self.suboffers if s.active]
	
	@property
	def categories_ids(self):
		return [category.id for category in self.categories]
	
	@property
	def women_categories(self):
		result = []
		for category in self.categories:
			if category.id in self._women_categories_ids:
				category.css_class = self._women_categories_css[self._women_categories_ids.index(category.id)]
				result.append(category)
		return result
	
	@property
	def not_women_categories(self):
		return [category for category in self.categories if category not in self.women_categories]

	@property
	def logo(self):
		return os.path.join(self._logos_dir, self.logo_filename) if self.logo_filename else None
	
	def owned_by(self, user):
		return self.advertiser.id == user.id
	
	def suboffer_by_id(self, suboffer_id):
		for suboffer in self.all_suboffers:
			if suboffer.id == suboffer_id:
				return suboffer
		return None
	
	def banner_by_id(self, banner_id):
		for banner in self.banners:
			if banner.id == banner_id:
				return banner
		return None
	
	@property
	def launched(self):
		return datetime.now() >= self.launch_time
	
	@property
	def visible(self):
		return self.approved and self.active and self.launched
	
	@property
	def regions_full(self):
		regions_dict = regions_repo.as_dict()
		regions = [regions_dict.get(code) for code in self.regions if code in regions_dict] 
		return sorted(regions, key=lambda r: r.country_name)
	
	def tracking_url(self, host_url, aff_id, banner_id=None):
		return u'{0}?method=track&offer_id={1}&aff_id={2}{3}'.format(
			os.path.join(host_url, u'api'), self.id, aff_id,
			u'&banner_id={0}'.format(banner_id) if banner_id else u''
		)
	
	def click_url(self, host_url, aff_id, banner_id=None):
		return u'{0}?method=click&offer_id={1}&aff_id={2}{3}'.format(
			os.path.join(host_url, u'api'), self.id, aff_id,
			u'&banner_id={0}'.format(banner_id) if banner_id else u''
		)


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
	
	@property
	def admin_moderation(self): return self.blocked and not self.block_reason


class Banner(IdentifiableModel):
	width = Field(types.Integer, 'width')
	height = Field(types.Integer, 'height')
	mime_type = Field(types.String, 'mime-type')
	url = Field(types.String, 'url')
	
	_mime_to_formats = {
		u'image/png': u'PNG',
		u'image/gif': u'GIF',
		u'image/jpeg': u'JPEG',
		u'application/x-shockwave-flash': u'Flash',
		u'application/svg+xml': u'SVG'
	}
	
	_banners_url = app.config.get('TRACKER_BANNERS_URL')
	
	@property
	def size(self): return u'{0} x {1}'.format(self.width, self.height)
	
	@property
	def format(self): return self._mime_to_formats.get(self.mime_type, 'UNKNOWN')
	
	@property
	def image_url(self): return os.path.join(self._banners_url, str(self.id))
	
	@property
	def has_code(self): return 'image' in self.mime_type


class Category(IdentifiableModel):
	name = Field(types.String, 'name')
	grouping_id = Field(types.Integer, 'grouping/@id')
	grouping = Field(types.String, 'grouping')


class CategoryGroup(IdentifiableModel):
	name = Field(types.String, '@name')
	categories = FieldList('Category', 'category')


class Region(models.ModelBase):
	country_code = Field(types.String, 'country-code')
	country_name = Field(types.String, 'country-name')


class OfferAction(IdentifiableModel):
	affiliate = Field('User', 'affiliate')
	offer = Field('Offer', 'offer')
	transaction_id = Field(types.String, 'transaction-id')
	state = Field(enums.OfferActionStates, 'state')
	creation_time = Field(types.DateTime, 'creation-time')
	last_change_time = Field(types.DateTime, 'last-change-time')
	amount = Field(types.Decimal, 'amount', quantize='1.00')
	
	@property
	def is_not_approved(self):
		return self.state == enums.OfferActionStates.NOT_APPROVED


class OverallOfferStat(models.ModelBase):
	id = Field(types.Integer, 'id')
	name = Field(types.String, 'name')
	exclusive = Field(types.Boolean, 'exclusive')
	shows = Field(types.Integer, 'shows')
	clicks = Field(types.Integer, 'clicks')
	leads = Field(types.Integer, 'leads')
	sales = Field(types.Integer, 'sales')
	confirmed_revenue = Field(types.Decimal, 'confirmed-revenue', quantize='1.00')
	not_confirmed_revenue = Field(types.Decimal, 'not-confirmed-revenue', quantize='1.00')
	cancelled_revenue = Field(types.Decimal, 'canceled-revenue', quantize='1.00')
	ctr = Field(types.Decimal, 'ctr', quantize='1.00')
	cr = Field(types.Decimal, 'cr', quantize='1.00')
	ecpc = Field(types.Decimal, 'ecpc', quantize='1.00')
	ecpm = Field(types.Decimal, 'ecpm', quantize='1.00')


class TotalStatPart(models.ModelBase):
	affiliate = Field(types.Decimal, 'affiliate')
	fee = Field(types.Decimal, 'fee')
	sum = Field(types.Decimal, 'sum')

class TotalStat(models.ModelBase):
	confirmed = Field('TotalStatPart', 'confirmed')
	not_confirmed = Field('TotalStatPart', 'not-confirmed')
	expired = Field('TotalStatPart', 'expired')
	canceled = Field('TotalStatPart', 'canceled')


class ApiError(IdentifiableModel):
	description = Field(types.String, 'description')
	uri = Field(types.String, 'uri')
	last_occurred = Field(types.DateTime, 'last-occurred')
	occurrence_count = Field(types.Integer, 'occurrence-count')
	stack_trace = Field(types.String, 'stack-trace')


class AffiliateTopEntry(models.ModelBase):
	id = Field(types.Integer, 'id')
	email = Field(types.String, 'email')
	amount = Field(types.Decimal, 'amount')
	conversion_rate = Field(types.Decimal, 'conversion_rate')


class Debt(models.ModelBase):
	user_id = Field(types.Integer, 'user-id')
	user_email = Field(types.String, 'user-email')
	user_wmr = Field(types.String, 'user-wmr')
	offer_id = Field(types.Integer, 'offer-id')
	offer_name = Field(types.String, 'offer-name')
	basis = Field(enums.WithdrawalBases, 'basis')
	order_time = Field(types.DateTime, 'order-time')
	payed_out_amount = Field(types.Decimal, 'payed-out-amount', quantize='1.00')
	debt_amount = Field(types.Decimal, 'debt-amount', quantize='1.00')
	income_amount = Field(types.Decimal, 'income-amount', quantize='1.00')
	available_for_order_amount = Field(types.Decimal, 'available-for-order-amount', quantize='1.00')
	ordered_amount = Field(types.Decimal, 'ordered-amount', quantize='1.00')
	pending_amount = Field(types.Decimal, 'pending-amount', quantize='1.00')
	
	@property
	def is_affiliate_revenue(self):
		return self.basis == enums.WithdrawalBases.AFFILIATE_REVENUE
	
	@property
	def is_fee(self):
		return self.basis == enums.WithdrawalBases.FEE


class UserStat(models.ModelBase):
	affiliate = Field('User', 'affiliate')
	clicks = Field(types.Integer, 'clicks')
	actions = Field(types.Integer, 'actions')
	conversion = Field(types.Decimal, 'conversion', quantize='1.00')
	canceled = Field(types.Integer, 'canceled')
	approved = Field(types.Integer, 'approved')
	not_confirmed = Field(types.Integer, 'not-confirmed')
	rate = Field(types.Decimal, 'rate', quantize='1.00')


class ReferralStat(models.ModelBase):
	id = Field(types.Integer, 'id')
	email = Field(types.String, 'email')
	register_time = Field(types.DateTime, 'register_time')
	source = Field(types.String, 'source')
	amount = Field(types.Decimal, 'amount', quantize='1.00')


class ReferralStatList(models.ModelBase):
	count = Field(types.Integer, '@count')
	sum = Field(types.Decimal, '@sum', quantize='1.00')
	items = FieldList('ReferralStat', 'stat')


class Product(IdentifiableModel):
	name = Field(types.String, 'name')
	model = Field(types.String, 'model')
	url = Field(types.String, 'url')
	picture = Field(types.String, 'picture')
	price = Field(types.Decimal, 'price', quantize='1.00')
	currency_id = Field(types.String, 'currencyId')
	category_id = Field(types.Integer, 'categoryId')
	description = Field(types.String, 'description')
	vendor = Field(types.String, 'vendor')
	vendor_code = Field(types.String, 'vendorCode')
	store = Field(types.Boolean, 'store')
	pickup = Field(types.Boolean, 'pickup')
	delivery = Field(types.Boolean, 'delivery')

	offer_id = Field(types.Integer, 'param[@name="hm_offer_id"]')
	offer_name = Field(types.String, 'param[@name="hm_offer_name"]')
	original_url = Field(types.String, 'param[@name="hm_original_url"]')


class YmlCatalog(models.ModelBase):
	products = FieldList('Product', 'shop/offers/offer')


class ShopCategory(IdentifiableModel):
	parent_id = Field(types.Integer, '@parentId')
	name = Field(types.String, '.')


class Shop(IdentifiableModel):
	name = Field(types.String, 'name')
	categories = FieldList('ShopCategory', 'categories/category')

	@property
	def categories_dict(self):
		if hasattr(self, '_categories_dict'):
			return self._categories_dict
		self._categories_dict = dict([(c.id, c) for c in self.categories])
		return self._categories_dict

	@property
	def categories_tree(self):
		if hasattr(self, '_categories_tree'):
			return self._categories_tree
		categories_dict = self.categories_dict
		self._categories_tree = []
		for category in self.categories:
			category.children = []
		for category in self.categories:
			if category.parent_id:
				categories_dict[category.parent_id].children.append(category)
			else:
				self._categories_tree.append(category)
		return self._categories_tree


registry.register_models_from_module(__name__)