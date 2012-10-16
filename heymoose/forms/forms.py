# -*- coding: utf-8 -*-
from wtforms import Form as WTForm
from wtforms import FieldList, FormField, BooleanField, TextField, PasswordField, \
	IntegerField, DecimalField, TextAreaField, SelectField, HiddenField, DateTimeField
from wtforms.fields import Label
from heymoose import app, resource as rc
from heymoose.data import enums
from heymoose.filters import currency, currency_sign
from heymoose.utils.times import begin_of_day, end_of_day, relativedelta
from heymoose.utils.gen import generate_unique_filename, generate_uid
from heymoose.utils.convert import to_unixtime, datetime_nosec_format
from heymoose.utils.dicts import create_dict
from flask import g
from datetime import datetime
import validators
import fields as myfields
import random, hashlib, os


class Form(WTForm):
	def process(self, formdata=None, obj=None, **kwargs):
		if formdata is not None and not hasattr(formdata, 'getlist'):
			raise TypeError("formdata should be a multidict-type wrapper that supports the 'getlist' method")

		for name, field, in self._fields.iteritems():
			handler = getattr(self, 'get_' + name, None)
			if obj is not None and handler is not None:
				field.process(formdata, handler(obj))
			elif obj is not None and hasattr(obj, name):
				field.process(formdata, getattr(obj, name))
			elif name in kwargs:
				field.process(formdata, kwargs[name])
			else:
				field.process(formdata)
	
	def populate_obj(self, obj):
		for name, field in self._fields.iteritems():
			handler = getattr(self, 'populate_' + name, field.populate_obj)
			handler(obj, name)


class CaptchaForm(Form):
	captcha = TextField(u'', [
		validators.Required(message=u'Введите число')
	], description=u'(докажите, что вы не робот)')
	ch = HiddenField()
	
	def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
		super(CaptchaForm, self).__init__(formdata, obj, prefix, **kwargs)
		if (formdata is None or 'ch' not in formdata) and obj is None:
			self.regenerate()
				
	def validate_captcha(self, field):
		answer = self.ch.data
		guess = self.generate_hash(self.captcha.data)
		self.regenerate()
		
		if guess != answer:
			raise ValueError(u'Ответ неверный, попробуйте еще раз')
			
	def regenerate(self):
		first = random.randrange(1000, 9000)
		second = random.randrange(1, 9)
		self.captcha.label = Label(self.captcha.id, u'{0} + {1} = ?'.format(first, second))
		self.captcha.data = u''
		self.ch.data = self.generate_hash(first + second)
		
	def generate_hash(self, value):
		m = hashlib.md5()
		m.update(u'hey{0}moo{1}se'.format(value, self.captcha.id))
		return m.hexdigest()
			

class LoginForm(Form):
	username = TextField(u'E-mail', [validators.Required(message = u'Введите электронный адрес')])
	password = PasswordField(u'Пароль', [validators.Required(message = u'Введите пароль')])
	remember = BooleanField(u'Запомнить меня', default=False)


class ForgottenPasswordForm(CaptchaForm):
	email = TextField(u'E-mail', [validators.Required(message = u'Введите электронный адрес')])


class UserRegisterFormMixin:
	password = PasswordField(u'Пароль', [
		validators.Length(min=4, max=16, message = u'Длина пароля должна быть от 4 до 16 символов'),
		validators.Required(message = u'Введите пароль')
	])
	password2 = PasswordField(u'Повторите пароль', [
		validators.Length(min=4, max=16, message = u'Длина пароля должна быть от 4 до 16 символов'),
		validators.EqualTo('password', message = u'Введенные пароли не совпадают'),
		validators.Required(message = u'Введите пароль повторно')
	])
	email = TextField(u'E-mail', [
		validators.Email(message = u'Некорректный адрес электронной почты'),
		validators.Required(message = u'Введите адрес электронной почты'),
		validators.check_email_not_registered
	])
	
	def populate_password(self, obj, name):
		obj.change_password(self.password.data)


class UserEditFormMixin:
	first_name = TextField(u'Ваше имя', [
		validators.Length(min=2, max=200, message = u'Имя может иметь длину от 2 до 200 символов'),
		validators.Optional()
	])
	last_name = TextField(u'Ваша фамилия', [
		validators.Length(min=2, max=200, message = u'Фамилия может иметь длину от 2 до 200 символов'),
		validators.Optional()
	])
	messenger_type = myfields.SelectField(u'Мессенджер', choices=[
		('', u'(не указывать)'),
		('SKYPE', u'Skype'),
		('JABBER', u'Jabber'),
		('ICQ', u'ICQ')
	], validators=[validators.Optional()])
	messenger_uid = myfields.TextField(u'UID в мессенджере')
	
	def validate_messenger_uid(self, field):
		if not self.messenger_type.data: return
		if not field.data:
			raise ValueError(u'Введите UID в выбранном вами мессенджере')
		elif not (2 <= len(field.data) <= 30):
			raise ValueError(u'UID может иметь длину от 2 до 30 символов')
	

class AdvertiserFormMixin:
	organization = myfields.TextField(u'Название организации', [
		validators.Length(max=200, message=u'Название организации не может быть длиннее 200 символов'),
		validators.Required(message=u'Введите название организации')
	])
	phone = TextField(u'Телефон', [
		validators.Length(min=5, max=30, message=u'Телефон может иметь длину от 5 до 30 исмволов'),
		validators.Required(message=u'Введите ваш телефон')
	])


class AdvertiserEditFormMixin(AdvertiserFormMixin):
	pass


class AffiliateFormMixin:
	organization = myfields.TextField(u'Название организации', [
		validators.Length(max=200, message=u'Название организации не может быть длиннее 200 символов'),
		validators.Optional()
	])
	phone = TextField(u'Телефон', [
		validators.Length(min=5, max=30, message=u'Телефон может иметь длину от 5 до 30 исмволов'),
		validators.Optional()
	])


class AffiliateEditFormMixin(AffiliateFormMixin):
	wmr = myfields.TextField(u'Ваш WMR-кошелёк', [
		validators.Required(message=u'Введите номер вашего WMR-кошелька')
	])

class AffiliateRegisterForm(CaptchaForm, UserRegisterFormMixin):
	pass

class AdvertiserRegisterForm(CaptchaForm, UserRegisterFormMixin, AdvertiserFormMixin):
	pass

class AffiliateEditForm(Form, UserEditFormMixin, AffiliateEditFormMixin):
	pass

class AdvertiserEditForm(Form, UserEditFormMixin, AdvertiserEditFormMixin):
	pass


class AdminUserFormMixin:
	email = TextField(u'E-mail', [
		validators.Email(message = u'Некорректный адрес электронной почты'),
		validators.Required(message = u'Введите адрес электронной почты')
	])
	confirmed = BooleanField(u'Подтвержден', default=False)
	
	def validate_email(self, field):
		if hasattr(self, 'user') and self.user.email != self.email.data:
			validators.check_email_not_registered(self, self.email)


class AdminAffiliateEditForm(AffiliateEditForm, AdminUserFormMixin):
	pass


class AdminAdvertiserEditForm(AdvertiserEditForm, AdminUserFormMixin):
	pass


class AdminPasswordChangeForm(Form):
	password = PasswordField(u'Новый пароль', [
		validators.Length(min=4, max=16, message=u'Длина пароля должна быть от 4 до 16 символов'),
		validators.Required(message=u'Введите пароль')
	])
	password2 = PasswordField(u'Повторите новый пароль', [
		validators.Length(min=4, max=16, message=u'Длина пароля должна быть от 4 до 16 символов'),
		validators.EqualTo('password', message=u'Введенные пароли не совпадают'),
		validators.Required(message=u'Введите пароль повторно')
	])
	
	def populate_password(self, obj, name):
		obj.change_password(self.password.data)


class PasswordChangeForm(AdminPasswordChangeForm):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordChangeForm, self).__init__(*args, **kwargs)
	
	oldpassword = PasswordField(u'Текущий пароль', [
		validators.Required(message=u'Введите текущий пароль'),
		validators.check_password
	])

class WMRForm(Form):
	wmr = myfields.TextField(u'Ваш WMR-кошелёк', [
		validators.Required(message=u'Введите номер вашего WMR-кошелька')
	])


class EmailNotifyForm(Form):
	mail = BooleanField(u'Письмо пользователю', default=True)


class UserBlockForm(EmailNotifyForm):
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=(u'Причина должна быть длиной не более 500 символов'))
	])

class OfferBlockForm(Form):
	notify = BooleanField(u'Уведомить рекламодателя и партнеров', default=True)
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=(u'Причина должна быть длиной не более 500 символов'))
	])


class ContactForm(CaptchaForm):
	name = TextField(u'Ваше имя', [
		validators.Required(message=u'Представьтесь, пожалуйста')			
	])
	email = TextField(u'Ваш e-mail', [
		validators.Email(message=u'Некорректный email-адрес'),
		validators.Required(message=u'Введите email адрес')
	])
	phone = TextField(u'Ваш телефон')
	desc = TextAreaField(u'Вопрос или сообщение')


class SiteForm(Form):
	name = TextField(u'Название площадки', [
		validators.Length(min=1, max=100, message=u'Название должно иметь длину от 1 до 100 символов'),
		validators.Required(message=u'Введите название площадки')
	])
	url = TextField(u'Адрес площадки', [
		validators.Required(message=u'Введите URL'),
		validators.URI(message=u'Введите URL в формате http://*.*', verify_exists=False)
	], default=u'http://')
	language = SelectField(u'Язык площадки', default=u'', choices=[
		(u'', u'(не указывать)'),
		(u'1', u'Русский'),
		(u'2', u'Английский'),
		(u'3', u'Немецкий')
	])
	uniqs = IntegerField(u'уникальных посетителей', [
		validators.Integer(message=u'Введите число'),
		validators.NumberRange(min=0, message=u'Укажите неотрицательное целое число')
	])
	views = IntegerField(u'просмотров', [
		validators.Integer(message=u'Введите число'),
		validators.NumberRange(min=0, message=u'Укажите неотрицательное целое число')
	])
	description = TextAreaField(u'Описание площадки', [
		validators.Length(min=100, message=u'Описание площадки должно содержать минимум 100 символов'),
		validators.Required(message=u'Введите описание площадки')
	])
	categories = myfields.CategoriesField(u'Категории', default=True)
	regions = myfields.CheckboxListField(u'Регионы', [
		validators.Required(message=u'Выберите хотя бы один регион')
	], choices=enums.Regions.tuples('name'), coerce=int, default=(enums.Regions.RUSSIA,))
	comment = TextAreaField(u'Комментарий для администрации')


class SubOfferForm(Form):
	title = TextField(u'Описание', [
		validators.Length(min=1, max=50, message=u'Описание должно иметь длину от 1 до 50 символов'),
		validators.Required(message=u'Введите описание действия')
	])
	payment_type = SelectField(u'Тип оплаты', choices=[
		(1, u'Фиксированная за действие'),
		(2, u'Фиксированная за первое действие и за последующие'),
		(3, u'Процент с заказа или покупки')
	], coerce=int)
	payment_value = DecimalField(u'Размер выплаты', [
		validators.NumberRange(min=0.00, message=u'Введите положительное число'),
	], default=1.00)
	cost2 = DecimalField(u'', [validators.Optional()], default=1.0)
	reentrant = BooleanField(u'многократ. прохождение', default=True)
	hold_days = IntegerField(u'Время холда', [
		validators.NumberRange(min=0, max=180, message=u'Время холда должно быть в интервале от 0 до 180 дней'),
		validators.Required(message=u'Введите время холда')
	], default=30)
	code = TextField(u'Код', [
		validators.Length(max=10, message=u'Код может быть длиной от 1 до 10 символов'),
		validators.Optional()
	])
	manual_code = BooleanField(u'указать код вручную', default=False)

	def validate_code(self, field):
		if self.manual_code.data and not self.code.data:
			raise ValueError(u'Введите код вручную')
		offer_id = getattr(self, 'offer_id', None)
		kwargs = dict(offer_id=offer_id) if offer_id else dict()
		if self.code.data and not rc.offers.check_code(g.user.id, self.code.data, **kwargs):
			raise ValueError(u'У вас уже имеется оффер с таким кодом')

	def generate_code(self):
		return u'{0}{1}'.format(g.user.id, generate_uid(5))

	def populate_code(self, obj, name):
		if self.code.data:
			code = self.code.data
		else:
			code = self.generate_code()
			while not rc.offers.check_code(g.user.id, code):
				code = self.generate_code()
		obj.code = code
	
	def get_manual_code(self, obj):
		return True if obj.code else False
	
	def get_payment_type(self, obj):
		if obj.pay_method and obj.pay_method == enums.PayMethods.CPC:
			return 0
		elif obj.cpa_policy == enums.CpaPolicies.FIXED:
			return 1
		elif obj.cpa_policy == enums.CpaPolicies.DOUBLE_FIXED:
			return 2
		else:
			return 3
		
	def populate_payment_type(self, obj, name):
		if self.payment_type.data == 0:
			obj.pay_method = enums.PayMethods.CPC
		else:
			obj.pay_method = enums.PayMethods.CPA
			if self.payment_type.data == 1:	
				obj.cpa_policy = enums.CpaPolicies.FIXED
			elif self.payment_type.data == 2:
				obj.cpa_policy = enums.CpaPolicies.DOUBLE_FIXED
			else:
				obj.cpa_policy = enums.CpaPolicies.PERCENT
	
	def get_payment_value(self, obj):
		return obj.cost or obj.percent
	
	def populate_payment_value(self, obj, name):
		if self.payment_type.data in (0, 1, 2):
			obj.cost = self.payment_value.data
			obj.percent = None
		else:
			obj.percent = self.payment_value.data
			obj.cost = None
	
	def validate_cost2(self, field):
		if self.payment_type.data == 2 and (self.cost2.data is None or self.cost2.data <= 0):
			raise ValueError(u'Введите положительное число')


class MainSubOfferForm(SubOfferForm):
	def __init__(self, *args, **kwargs):
		super(MainSubOfferForm, self).__init__(*args, **kwargs)
		self.payment_type.choices = [(0, u'Фиксированная за клик')] + self.payment_type.choices

class AdminSubOfferEditForm(SubOfferForm):
	active = BooleanField(u'Активно', default=True)

class OfferFormBase(Form):
	name = TextField(u'Название оффера', [
		validators.Length(min=1, max=100, message=u'Название должно иметь длину от 1 до 100 символов'),
		validators.Required(message=u'Введите название оффера')
	])
	site_url = TextField(u'Ссылка на сайт рекламодателя', [
		validators.Required(message=u'Введите URL'),
		validators.URI(message=u'Введите URL в формате http://*.*', verify_exists=False)
	], default=u'http://')
	url = TextField(u'Партнерская ссылка', [
		validators.Required(message=u'Введите URL'),
		validators.URI(message=u'Введите URL в формате http://*.*', verify_exists=False)
	], default=u'http://')
	logo = myfields.ImageField(u'Логотип', [
		validators.FileFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	])
	short_description = TextAreaField(u'Краткое описание кампании', [
		validators.Required(message=u'Введите краткое описание кампании'),
		validators.Length(min=1, max=250, message=u'Краткое описание должно иметь длину до 250 символов')
	])
	description = TextAreaField(u'Подробное описание', [
		validators.Required(message=u'Введите описание кампании')
	])
	launch_time = DateTimeField(u'Дата запуска', format='%d.%m.%Y', validators=[
		validators.Required(message=u'Введите дату запуска оффера')
	], default=datetime.now)
	allow_deeplink = BooleanField(u'Разрешить deeplink', default=False)
	cookie_ttl = IntegerField(u'Время жизни Cookie', [
		validators.Required(message=u'Введите время жизни cookie'),
		validators.NumberRange(min=0, message=u'Время жизни должно быть больше нуля')
	], default=30)
	categories = myfields.CategoriesField(u'Категории', default=False)
	regions = myfields.RegionsField(u'Регионы',
		predefined=('RU', 'UA', 'BY', 'KZ', 'AM', 'AZ', 'KG', 'MD', 'TJ', 'TM', 'UZ')
	)
	targeting = BooleanField(u'включить геотаргетинг', default=False)
	traffic = myfields.CheckboxListField(u'Типы трафика', choices=[
		(0, u'Cashback'),
		(1, u'PopUp-реклама'),
		(2, u'Контекстная реклама'),
		(3, u'Дорвей-трафик'),
		(4, u'Email-рассылка'),
		(5, u'Контекстная реклама на бренд'),
		(6, u'Трафик с социальных сетей')
	], coerce=int)

	logo_max_size = (150, 100)
	logos_path = os.path.join(app.config.get('UPLOAD_PATH'), app.config.get('OFFER_LOGOS_DIR'))
	def populate_logo(self, obj, name):
		if not self.logo.data: return
		obj.logo_filename = '{0}.{1}'.format(generate_unique_filename(), self.logo.format)
		self.logo.data.thumbnail(self.logo_max_size, 1) # 1 == Image.ANTIALIAS
		self.logo.data.save(os.path.join(self.logos_path, obj.logo_filename))

class OfferForm(OfferFormBase):	
	main_suboffer = FormField(MainSubOfferForm)
	suboffers = FieldList(FormField(SubOfferForm))
	
	def populate_main_suboffer(self, obj, name):
		self.main_suboffer.form.populate_obj(obj)
	
	def populate_suboffers(self, obj, name):
		pass

class OfferEditForm(OfferFormBase):
	token_param_name = TextField(u'Название параметра токена', [
		validators.Length(min=1, max=20, message=u'Название параметра должно иметь длину от 1 до 20 символов'),
		validators.Required(message=u'Введите название параметра токена')
	])

class AdminOfferEditForm(OfferEditForm):
	cr = DecimalField(u'Конверсия', [
		validators.Optional(),
		validators.NumberRange(min=0.00, max=100.00, message=u'Конверсия может быть от 0% до 100%'),
	])
	showcase = BooleanField(u'Отображать в витрине', default=False)


class OfferRequestDecisionForm(Form):
	action = HiddenField()
	grant_id = HiddenField()
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=u'Причина должна быть длиной не более 500 символов')
	])


class AdminOfferRequestDecisionForm(OfferRequestDecisionForm):
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=u'Причина должна быть длиной не более 500 символов')
	], default=u'Ваш способ продвижения не подходит для данной рекламной кампании')
	notify = BooleanField(u'уведомить партнёра', default=True)


class OfferGrantForm(Form):
	back_url = TextField(u'Back URL', [
		validators.URI(message=u'Введите URL в формате http://*.*', verify_exists=False),
		validators.Optional()
	])
	postback_url = TextField(u'Postback URL', [
		validators.URI(message=u'Введите URL в формате http://*.*', verify_exists=False),
		validators.Optional()
	])


class OfferBannerForm(Form):
	image = myfields.BannerField(u'Выберите изображение', [
		validators.FileRequired(message=u'Выберите файл на диске'),
		validators.FileFormat(formats=('jpg', 'jpeg', 'gif', 'png', 'swf', 'svg'),
			message=u'Выберите изображение в формате JPG, GIF или PNG')
	])
	
	def populate_image(self, obj, name):
		obj.width = self.image.width
		obj.height = self.image.height
		obj.mime_type = self.image.mime_type

	
class BalanceForm(Form):
	amount = DecimalField(u'Сумма', [
		validators.Required(message = u'Укажите сумму в {0}'.format(currency_sign)),
		validators.NumberRange(min=1, max=60000000, message=u'Такая сумма недопустима')
	], description=currency_sign, places=2)


class DateTimeRangeForm(Form):
	dt_from = DateTimeField(u'с', format='%d.%m.%Y %H:%M', validators=[
		validators.Required(message=u'Введите время')
	], default=lambda: begin_of_day(datetime.now()) + relativedelta(months=-1, days=+1))
	dt_to = DateTimeField(u'по', format='%d.%m.%Y %H:%M', validators=[
		validators.Required(message=u'Введите время')
	], default=lambda: end_of_day(datetime.now()))
	
	def range_args(self):
		return {'from' : to_unixtime(self.dt_from.data, True), 'to' : to_unixtime(self.dt_to.data, True)}
	
	def backend_args(self):
		return self.range_args()
	
	def query_args(self):
		return dict(dt_from=self.dt_from.data.strftime(datetime_nosec_format),
			dt_to=self.dt_to.data.strftime(datetime_nosec_format))


class OfferStatsFilterForm(DateTimeRangeForm):
	requested = BooleanField(u'только с заявками', default=False)
	
	def query_args(self):
		args = DateTimeRangeForm.query_args(self)
		if self.requested.data:	args.update(requested=u'y')
		return args
	
	def backend_args(self):
		args = DateTimeRangeForm.backend_args(self)
		args.update(granted=self.requested.data)
		return args


class CabinetStatsForm(DateTimeRangeForm):
	offer = myfields.OfferField(u'Оффер', coerce=int, default=0)
	
	def query_args(self):
		args = super(CabinetStatsForm, self).query_args()
		args.update(offer=self.offer.data)
		return args
	
	def backend_args(self):
		args = super(CabinetStatsForm, self).backend_args()
		if self.offer.data: args.update(offer_id=self.offer.data)
		return args


class CabinetSubIdStatsForm(CabinetStatsForm):
	sub_id = TextField(u'SubID')
	sub_id1 = TextField(u'SubID')
	sub_id2 = TextField(u'SubID')
	sub_id3 = TextField(u'SubID')
	sub_id4 = TextField(u'SubID')
	g_sub_id = BooleanField(u'Группировать по SubID')
	g_sub_id1 = BooleanField(u'Группировать по SubID1')
	g_sub_id2 = BooleanField(u'Группировать по SubID2')
	g_sub_id3 = BooleanField(u'Группировать по SubID3')
	g_sub_id4 = BooleanField(u'Группировать по SubID4')
		
	def query_args(self):
		args = super(CabinetSubIdStatsForm, self).query_args()
		args.update(sub_id=self.sub_id.data, sub_id1=self.sub_id1.data, 
			sub_id2=self.sub_id2.data, sub_id3=self.sub_id3.data, sub_id4=self.sub_id4.data)
		if self.g_sub_id.data: args.update(g_sub_id=u'y')
		if self.g_sub_id1.data: args.update(g_sub_id1=u'y')
		if self.g_sub_id2.data: args.update(g_sub_id2=u'y')
		if self.g_sub_id3.data: args.update(g_sub_id3=u'y')
		if self.g_sub_id4.data: args.update(g_sub_id4=u'y')
		return args
	
	def backend_args(self):
		args = super(CabinetSubIdStatsForm, self).backend_args()
		args.update(g_sub_id=self.g_sub_id.data, g_sub_id1=self.g_sub_id1.data,
			g_sub_id2=self.g_sub_id2.data, g_sub_id3=self.g_sub_id3.data,
			g_sub_id4=self.g_sub_id4.data)
		if self.sub_id.data: args.update(sub_id=self.sub_id.data)
		if self.sub_id1.data: args.update(sub_id1=self.sub_id1.data)
		if self.sub_id2.data: args.update(sub_id2=self.sub_id2.data)
		if self.sub_id3.data: args.update(sub_id3=self.sub_id3.data)
		if self.sub_id4.data: args.update(sub_id4=self.sub_id4.data)
		return args
	
	@property
	def groupings(self):
		return [self.g_sub_id.data, self.g_sub_id1.data, self.g_sub_id2.data, self.g_sub_id3.data, self.g_sub_id4.data]
	
	def sub_ids_from_string(self, string, delimeter='/'):
		rv = dict()
		if not string: return rv
		sub_ids = [sub_id.strip() for sub_id in string.split('/')]
		index = 0
		for i, grouping in enumerate(self.groupings):
			if grouping:
				rv.update({'sub_id{0}'.format(i or '') : sub_ids[index]})
				index += 1
		return rv


class OfferActionsFilterForm(DateTimeRangeForm):
	date_kind = SelectField(u'Время', choices=enums.OfferActionDateKinds.tuples('name'),
		default=enums.OfferActionDateKinds.CREATION)
	state = SelectField(u'Состояние', choices=[(u'', u'(все)')] + enums.OfferActionStates.tuples('name'), default=u'')
	
	def query_args(self):
		args = DateTimeRangeForm.query_args(self)
		args.update(state=self.state.data, date_kind=self.date_kind.data)
		return args
	
	def backend_args(self):
		args = DateTimeRangeForm.backend_args(self)
		args.update(date_kind=self.date_kind.data)
		if self.state.data: args.update(state=self.state.data)
		return args


class DebtFilterForm(DateTimeRangeForm):
	date_kind = SelectField(u'Время', choices=enums.DebtDateKinds.tuples('name'),
		default=enums.DebtDateKinds.CREATION)

	def query_args(self):
		args = DateTimeRangeForm.query_args(self)
		args.update(date_kind=self.date_kind.data)
		return args

	def backend_args(self):
		args = DateTimeRangeForm.backend_args(self)
		args.update(date_kind=self.date_kind.data)
		return args


class PaymentFilterForm(DateTimeRangeForm):
	method = SelectField(u'Способ оплаты',
		choices=[
			(u'', u'(все)'),
			(u'AUTO', u'автоматически'),
			(u'MANUAL', u'вручную')
		], default=u'')

	def query_args(self):
		args = DateTimeRangeForm.query_args(self)
		args.update(method=self.method.data)
		return args

	def backend_args(self):
		args = DateTimeRangeForm.backend_args(self)
		args.update(method=self.method.data)
		return args


class UserFilterForm(DateTimeRangeForm):
	active = BooleanField(u'только активные', default=True)

	def query_args(self):
		args = DateTimeRangeForm.query_args(self)
		if self.active.data: args.update(active=u'y')
		return args

	def backend_args(self):
		args = DateTimeRangeForm.backend_args(self)
		args.update(active=self.active.data)
		return args


class CategoryForm(Form):
	group = myfields.CategoryGroupField(u'Родительская категория')
	name = TextField(u'Название категории', [
		validators.Required(message=u'Введите название категории'),
		validators.Length(min=3, max=250, message=u'Название категории должно иметь длину от 3 до 250 символов')
	])


class OfferFilterForm(Form):
	payment_type = SelectField(u'Тип оплаты', choices=[
		(0, u'(любой)'),
		(1, u'Фиксированная за клик'),
		(2, u'Фиксированная за действие'),
		(3, u'Процент с заказа или покупки')
	], coerce=int, default=0)
	category = myfields.CategoriesField(u'Категории', default=False)
	region = myfields.RegionsField(u'Регионы',
		predefined=('RU', 'UA', 'BY', 'KZ', 'AM', 'AZ', 'KG', 'MD', 'TJ', 'TM', 'UZ')
	)
	exclusive_only = BooleanField(u'только эксклюзивные', default=False)
	
	def query_args(self):
		return create_dict(
			payment_type=self.payment_type.data,
			category=self.category.data,
			region=self.region.data,
			exclusive_only=u'y' if self.exclusive_only.data else None
		)
	
	def backend_args(self):
		return create_dict(
			category=self.category.data,
			region=self.region.data,
			pay_method=None if self.payment_type.data == 0 else
				enums.PayMethods.CPC if self.payment_type.data == 1 else enums.PayMethods.CPA,
			cpa_policy=None if self.payment_type.data in (0, 1) else
				enums.CpaPolicies.FIXED if self.payment_type.data == 2 else enums.CpaPolicies.PERCENT,
			exclusive=self.exclusive_only.data or None
		)
	
	def has_filled_fields(self):
		return self.region.data or self.category.data or self.payment_type.data > 0 or self.exclusive_only.data


class AdminOfferFilterForm(OfferFilterForm):
	active_only = BooleanField(u'только активные', default=False)

	def query_args(self):
		args = super(AdminOfferFilterForm, self).query_args()
		if self.active_only.data: args.update(active_only=u'y')
		return args

	def backend_args(self):
		args = super(AdminOfferFilterForm, self).backend_args()
		if self.active_only.data: args.update(approved=True, active=True)
		return args

	def has_filled_fields(self):
		return super(AdminOfferFilterForm, self).has_filled_fields() or self.active_only.data


class CatalogOfferFilterForm(OfferFilterForm):
	offset = IntegerField(u'', [validators.NumberRange(min=0)], default=0)
	exclusive = BooleanField(u'')
	
	def backend_args(self):
		args = super(CatalogOfferFilterForm, self).backend_args()
		args.update(offset=self.offset.data, limit=10)
		if self.exclusive.data: args.update(exclusive=True)
		return args


class NewsItemForm(Form):
	title = TextField(u'Заголовок', [
		validators.Required(message=u'Введите заголовок новости'),
		validators.Length(min=1, max=100, message=u'Заголовок может иметь длину от 1 до 100 символов')
	])
	summary = TextAreaField(u'Краткое описание', [
		validators.Length(max=180, message=u'Краткое описание может иметь длину до 180 символов')
	])
	text = TextAreaField(u'Текст', [
		validators.Required(message=u'Введите текст новости'),					
	])
	date = DateTimeField(u'Время публикации', format='%d.%m.%Y %H:%M', validators=[
		validators.Required(message=u'Введите время публикации')
	])
	image = myfields.ImageField(u'Изображение', [
		validators.FileFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	])
	on_main = BooleanField(u'Отображать на главной', default=False)
	active = BooleanField(u'Активна', default=True)
	
	image_max_size = (100, 100)
	images_path = os.path.join(app.config.get('UPLOAD_PATH'), app.config.get('NEWS_IMAGES_DIR'))
	def populate_image(self, obj, name):
		if not self.image.data: return
		obj.image = '{0}.{1}'.format(generate_unique_filename(), self.image.format)
		self.image.data.thumbnail(self.image_max_size, 1) # 1 == Image.ANTIALIAS
		self.image.data.save(os.path.join(self.images_path, obj.image))


notification_users_choices = [
	(0, u'(всем)'),
	(1, u'партнёрам'),
	(2, u'рекламодателям')
]

class NotificationForm(Form):
	text = TextAreaField(u'Текст уведомления', [validators.Required(message=u'Введите текст уведомления')])
	role = SelectField(u'Кому', choices=notification_users_choices, coerce=int)
	
	def backend_args(self):
		return dict(role=self.role.data) if self.role.data else dict()


poll_city_choices = [
	(u'Москва (МО)', u'Москва (МО)'),
	(u'Санкт-Петербург', u'Санкт-Петербург'),
	(u'Киев', u'Киев'),
	(u'Минск', u'Минск'),
	(u'', u'Другой...')
]

class PollCityForm(Form):
	city_select = SelectField(u'Город', choices=poll_city_choices)
	city_input = TextField(u'Город', [
		validators.Length(max=100, message=u'Название города должно иметь длину до 100 символов')
	])
	
	def validate_city_input(self, field):
		if not self.city_select.data and not self.city_input.data:
			raise ValueError(u'Введите название города')
