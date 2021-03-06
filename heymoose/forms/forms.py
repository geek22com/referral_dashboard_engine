# -*- coding: utf-8 -*-
from wtforms import Form as WTForm
from wtforms import FieldList, FormField, BooleanField, TextField, PasswordField, \
	IntegerField, DecimalField, TextAreaField, SelectField, HiddenField
from wtforms.fields import Label
from heymoose import app
from heymoose.core import actions
from heymoose.core.actions import roles
from heymoose.filters import currency, currency_sign
import validators
import fields as myfields
import random, hashlib


'''class Form(WTForm):
	def process(self, formdata=None, obj=None, **kwargs):
		if formdata is not None and not hasattr(formdata, 'getlist'):
			raise TypeError("formdata should be a multidict-type wrapper that supports the 'getlist' method")

		for name, field, in self._fields.iteritems():
			if obj is not None and hasattr(obj, name):
				field.process(formdata, getattr(obj, name))
			elif name in kwargs:
				field.process(formdata, kwargs[name])
			else:
				field.process(formdata)
	
	def populate_obj(self, obj):
		for name, field in self._fields.iteritems():
			handler = getattr(self, 'populate_' + name, field.populate_obj)
			handler(obj, name)'''
Form = WTForm


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
		self.captcha.label = Label(self.captcha.id, u'{0} + {1} ='.format(first, second))
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

class RoleForm(Form):
	role = SelectField('role', choices=[(roles.DEVELOPER, roles.DEVELOPER),
										(roles.CUSTOMER, roles.CUSTOMER)])


class UserFormBase(Form):
	first_name = TextField(u'Ваше имя', [
		validators.Length(min=2, max=200, message = u'Имя может иметь длину от 2 до 200 символов'),
		validators.Required(message = u'Введите ваше имя')
	])
	last_name = TextField(u'Ваша фамилия', [
		validators.Length(min=2, max=200, message = u'Фамилия может иметь длину от 2 до 200 символов'),
		validators.Required(message = u'Введите вашу фамилию')
	])
	organization = myfields.NullableTextField(u'Организация', [
		validators.Length(max=200, message = u'Название организации не может быть длиннее 200 символов'),
	])
	
class CustomerFormMixin:
	phone = TextField(u'Телефон', [
		validators.Length(min=5, max=30, message = u'Телефон может иметь длину от 5 до 30 исмволов'),
		validators.Required(message = u'Введите ваш телефон')
	])
	messenger_type = myfields.NullableSelectField(u'Мессенджер', choices=[
		('', u'(не указывать)'),
		('SKYPE', u'Skype'),
		('JABBER', u'Jabber'),
		('ICQ', u'ICQ')
	])
	messenger_uid = myfields.NullableTextField(u'UID в мессенджере')
	
	def validate_messenger_uid(self, field):
		if not self.messenger_type.data: return
		if not field.data:
			raise ValueError(u'Введите UID в выбранном вами мессенджере')
		elif not (2 <= len(field.data) <= 30):
			raise ValueError(u'UID может иметь длину от 2 до 30 символов')
		
class DeveloperFormMixin:
	phone = myfields.NullableTextField(u'Телефон')
	messenger_type = SelectField(u'Мессенджер', choices=[
		('SKYPE', u'Skype'),
		('JABBER', u'Jabber'),
		('ICQ', u'ICQ')
	], validators = [validators.Required(message = u'Запоните тип мессенджера')])
	messenger_uid = TextField(u'UID в мессенджере', [
		validators.Length(min=2, max=30, message = u'UID может иметь длину от 2 до 30 символов'),
		validators.Required(message = u'Введите UID в выбранном мессенджере')
	])

class RegisterForm(UserFormBase):
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
	
class DeveloperRegisterForm(RegisterForm, DeveloperFormMixin):
	invite = TextAreaField(u'Код приглашения', [
		validators.Required(message=u'Скопируйте сюда полученный код приглашения'),
		validators.check_invite
	])
	
class CustomerRegisterForm(RegisterForm, CustomerFormMixin):
	pass

class DeveloperEditForm(UserFormBase, DeveloperFormMixin):
	pass

class CustomerEditForm(UserFormBase, CustomerFormMixin):
	pass

class AdminUserEditFormMixin:
	email = TextField(u'E-mail', [
		validators.Email(message = u'Некорректный адрес электронной почты'),
		validators.Required(message = u'Введите адрес электронной почты')
	])
	confirmed = BooleanField(u'Подтвержден', default=False)
	
	def validate_email(self, field):
		if hasattr(self, 'user') and self.user.email != self.email.data:
			validators.check_email_not_registered(self, self.email)
	
class AdminDeveloperEditForm(DeveloperEditForm, AdminUserEditFormMixin):
	pass

class AdminCustomerEditForm(CustomerEditForm, AdminUserEditFormMixin):
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

class PasswordChangeForm(AdminPasswordChangeForm):
	oldpassword = PasswordField(u'Текущий пароль', [
		validators.Required(message=u'Введите текущий пароль'),
		validators.check_password
	])

class EmailNotifyForm(Form):
	mail = BooleanField(u'Письмо пользователю', default=True)

class UserBlockForm(EmailNotifyForm):
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=(u'Причина должна быть длиной не более 500 символов'))
	])
	
class OrderBlockForm(EmailNotifyForm):
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=(u'Причина должна быть длиной не более 500 символов'))
	], default=u'Заказ не соответствует правилам размещения рекламы в сети ВКонтакте.')
	
class WithdrawalDeleteForm(Form):
	reason = TextAreaField(u'Причина', [
		validators.Length(max=500, message=(u'Причина должна быть длиной не более 500 символов')),
		validators.Required(message=u'Введите причину отмены')
	])

class FeedBackForm(Form):
	feedback_email = TextField('Email Address', [
					  validators.Email("Некорректный email адресс")])
	feedback_comment = TextAreaField('Comment', [validators.Required(message = ('Напишите ваше пожелание') )])
	feedback_captcha_answer = TextField('captcha_answer', [validators.Required(message = ('Введите каптчу'))])

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
	
class PartnerContactForm(ContactForm):
	desc = TextAreaField(u'Описание вашей площадки')


class OrderForm(Form):
	ordername = TextField(u'Название заказа', [
		validators.Length(min=1, max=50, message=(u'Название заказа должно быть от 1 до 50 символов')),
		validators.Required(message = (u'Введите название заказа'))
	])
	orderurl = TextField(u'URL', [
		validators.Required(message = (u'Введите URL')),
		validators.URI(message = u'Введите URL в формате http://*.*', verify_exists=False)
	], default=u'http://')
	orderbalance = DecimalField(u'Баланс', [
		validators.Decimal(message=u'Введите число'),
		validators.NumberRange(min=0.0, message=u'Такой баланс недопустим'),
	], default=0.0)
	ordermale = SelectField(u'Пол', choices=[(u'True', u'мужской'), (u'False', u'женский'), (u'', u'любой')], default='')
	orderminage = myfields.NullableIntegerField(u'Минимальный возраст', [
		validators.NumberRangeOptional(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))
	])
	ordermaxage = myfields.NullableIntegerField(u'Максимальный возраст', [
		validators.NumberRangeOptional(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))
	])
	orderminhour = myfields.NullableIntegerField(u'Время с', [
		validators.NumberRangeOptional(min=0, max=23, message=(u'Введите час от 0 до 23'))
	])
	ordermaxhour = myfields.NullableIntegerField(u'Время до', [
		validators.NumberRangeOptional(min=0, max=23, message=(u'Введите час от 0 до 23'))
	])
	ordercitiesfilter = SelectField(u'Фильтр по городам', default=u'', choices=[
		(u'', u'не учитывать'),
		(u'INCLUSIVE', u'только указанные'),
		(u'EXCLUSIVE', u'все, кроме указанных')
	])
	ordercities = TextField(u'Список городов')
	
	def validate_orderbalance(self, field):
		balance = self.orderbalance.data
		if balance > 0.0 and round(balance, 2) == 0.0:
			raise ValueError(u'Такой баланс недопустим')
	
class AdminOrderFormMixin:
	orderautoapprove = BooleanField(u'Автоподтверждение', default=True)
	orderreentrant = BooleanField(u'Многократное прохождение', default=True,
		description=u'(разрешить одному пользователю проходить оффер много раз)'
	)
	orderallownegativebalance = BooleanField(u'Разрешить кредит', default=False, 
		description=u'(разрешить отрицательный баланс)'
	)
	
	
class RegularOrderForm(OrderForm):
	ordercpa = DecimalField(u'Стоимость действия (CPA)', [validators.Required(message=u'Введите CPA')])
	orderdesc = TextAreaField(u'Описание', [
		validators.Length(min=1, max=200, message=(u'Описание заказа должно быть от 1 до 200 символов')),
		validators.Required(message = (u'Введите описание'))
	])
	orderimage = myfields.ImageField(u'Выберите изображение', [
		validators.FileRequired(message=u'Выберите изображение на диске'),
		validators.FileFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	], description=u'Форматы: JPG (JPEG), GIF, PNG')
	
class RegularOrderEditFormBase(RegularOrderForm):
	def __init__(self, *args, **kwargs):
		super(RegularOrderEditFormBase, self).__init__(*args, **kwargs)
		del self.orderbalance
		self.orderimage.validators = self.orderimage.validators[:]
		for validator in self.orderimage.validators:
			if isinstance(validator, validators.FileRequired):
				self.orderimage.validators.remove(validator)
		self.orderimage.flags.required = False
		
class RegularOrderEditForm(RegularOrderEditFormBase):
	def __init__(self, *args, **kwargs):
		super(RegularOrderEditForm, self).__init__(*args, **kwargs)
		del self.orderurl
		
class AdminRegularOrderEditForm(RegularOrderEditFormBase, AdminOrderFormMixin):
	pass


class BannerOrderForm(OrderForm):
	ordercpa = DecimalField(u'Стоимость клика', [
		validators.Required(message=u'Введите стоимость клика')
	])
	orderbannersize = SelectField(u'Размер баннера', coerce=int)
	orderimage = myfields.BannerField(u'Выберите файл', [
		validators.FileRequired(message=u'Выберите файл на диске'),
		validators.FileFormat(formats=('jpg', 'jpeg', 'gif', 'png', 'swf', 'svg'),
			message=u'Выберите файл в формате JPG, GIF, PNG, SVG или SWF')
	])
	
	def __init__(self, *args, **kwargs):
		c_min = kwargs.pop('c_min', 0.01)
		c_rec = kwargs.pop('c_rec', None)
		if c_rec:
			kwargs.setdefault('ordercpa', c_rec)
		super(BannerOrderForm, self).__init__(*args, **kwargs)
		
		min_validator = validators.NumberRange(min=c_min,
			message=u'Стоимость клика не может быть меньше {0}'.format(currency(c_min)))
		if c_rec is not None:
			description = u'Минимальная {0}, рекомендуемая {1}'.format(currency(c_min), currency(c_rec))
		else:
			description = u'Минимальная {0}'.format(currency(c_min))
			
		self.ordercpa.validators = self.ordercpa.validators + [min_validator]
		self.ordercpa.description = description
			
	def validate_orderimage(self, field):
		if field.data is None: return
		size = actions.bannersizes.get_banner_size(self.orderbannersize.data)
		if field.width != size.width or field.height != size.height:
			raise ValueError(u'Размер баннера должен совпадать с указанным')
		
class BannerOrderEditFormBase(BannerOrderForm):
	def __init__(self, *args, **kwargs):
		super(BannerOrderEditFormBase, self).__init__(*args, **kwargs)
		del self.orderbalance
		del self.orderbannersize
		del self.orderimage
		
class BannerOrderEditForm(BannerOrderEditFormBase):
	def __init__(self, *args, **kwargs):
		super(BannerOrderEditForm, self).__init__(*args, **kwargs)
		del self.orderurl
		
class AdminBannerOrderEditForm(BannerOrderEditFormBase, AdminOrderFormMixin):
	ordercpa = DecimalField(u'Стоимость клика', [
		validators.NumberRange(min=0.1, message=u'Стоимость клика не может быть меньше 0.1'),
		validators.Required(message=u'Введите стоимость клика')
	])
	
		
class VideoOrderForm(OrderForm):
	ordercpa = DecimalField(u'Стоимость действия (CPA)', [validators.Required(message=u'Введите CPA')])
	ordervideourl = TextField(u'URL видеозаписи', [
		validators.Required(message = (u'Введите URL')),
		validators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
		
class VideoOrderEditFormBase(VideoOrderForm):
	def __init__(self, *args, **kwargs):
		super(VideoOrderEditFormBase, self).__init__(*args, **kwargs)
		del self.orderbalance

class VideoOrderEditForm(VideoOrderEditFormBase):
	def __init__(self, *args, **kwargs):
		super(VideoOrderEditForm, self).__init__(*args, **kwargs)
		del self.orderurl

class AdminVideoOrderEditForm(VideoOrderEditFormBase, AdminOrderFormMixin):
	pass


class OrderAppsForm(Form):
	filter = SelectField(u'Тип таргетинга', default=u'', choices=[
		(u'', u'не учитывать'),
		(u'INCLUSIVE', u'только указанные'),
		(u'EXCLUSIVE', u'все, кроме указанных')
	])
	apps = HiddenField()
	
	
class BannerForm(Form):
	size = SelectField(u'Размер баннера', coerce=int)
	image = myfields.BannerField(u'Выберите файл', [
		validators.FileRequired(message=u'Выберите файл на диске'),
		validators.FileFormat(formats=('jpg', 'jpeg', 'gif', 'png', 'swf', 'svg'),
			message=u'Выберите файл в формате JPG, GIF, PNG, SVG или SWF')
	])
	
	def validate_image(self, field):
		if field.data is None: return
		size = actions.bannersizes.get_banner_size(self.size.data)
		if field.width != size.width or field.height != size.height:
			raise ValueError(u'Размер баннера должен совпадать с указанным')
	
	
class BannerSizeForm(Form):
	width = IntegerField(u'Ширина', [
		validators.Required(message=u'Укажите ширину баннера'),
		validators.NumberRange(min=1, max=3000, message=u'Баннер может иметь ширину от 1 до 3000 пикселей')
	])
	height = IntegerField(u'Высота', [
		validators.Required(message=u'Укажите высоту баннера'),
		validators.NumberRange(min=1, max=3000, message=u'Баннер может иметь высоту от 1 до 3000 пикселей')
	])
	

class CityForm(Form):
	id = HiddenField(default=u'0')
	name = TextField(u'Название', [
		validators.Required(message=u'Введите название города'),
		validators.Length(min=2, max=100, message=(u'Название города должно содержать от 2 до 100 символов'))
	])
	
	
class AppForm(Form):
	apptitle = TextField(u'Название', [
		validators.Length(min=1, max=100, message=(u'Название приложения должно иметь длину от 1 до 100 символов')),
		validators.Required(message = (u'Введите название приложения'))
	])
	'''appcallback = TextField(u'Callback', [
		validators.Required(message = u'Введите callback для вашего приложения'),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])'''
	appurl = TextField(u'URL', [
		validators.Required(message = u'Введите URL для возврата в ваше приложение'),
		validators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	appplatform = SelectField(u'Платформа', choices=[
		('VKONTAKTE', u'ВКонтакте'),
		('FACEBOOK', u'Facebook'),
		('ODNOKLASSNIKI', u'Одноклассники')
	])
	
class AppEditForm(AppForm):
	pass

class AdminAppEditForm(AppEditForm):
	appd = DecimalField(u'Оплата за клик (D)', [
		validators.Decimal(message=u'Введите число'),
		validators.NumberRange(min=0.0, message=u'Такая сумма недопустима')
	], places=2)
	appt = DecimalField(u'Коэффициент надбавки (T)', [
		validators.Decimal(message=u'Введите число'),
		validators.NumberRange(min=0.0, message=u'Такой коэффициент недопустим')
	], description=u'K = D + (C - D)*T', places=2)
	appdeleted = BooleanField(u'Удалено', default=False)

	
class AppsShowDeletedForm(Form):
	show = BooleanField(u'Показывать удаленные приложения', default=False)
	dummy = HiddenField(default='1')
	
class BalanceForm(Form):
	amount = DecimalField(u'Сумма', [
		validators.Required(message = u'Укажите сумму в {0}'.format(currency_sign)),
		validators.NumberRange(min=1, max=60000000, message=u'Такая сумма недопустима')
	], description=currency_sign, places=2)
	
class OrderBalanceTransferForm(BalanceForm):
	order = SelectField(u'На счет заказа', coerce=int)


class TrafficAnalyzeForm(Form):
	cpc = DecimalField(u'Стоимость клика', [
		validators.Required(message=u'Введите стоимость клика'),
		validators.NumberRange(min=0.1, message=u'Такая стоимость недопустима')
	])


class SettingsForm(Form):
	min_cpc = app.config.get('MIN_CPC')
	
	c_min = DecimalField(u'Минимальная стоимость клика (Cmin)', [
		validators.Required(message=u'Введите Cmin'),
		validators.NumberRange(min=min_cpc, message=u'Такая стоимость недопустима')
	], description=u'Минимально допустимая стоимость {0}'.format(currency(min_cpc)))
	q = DecimalField(u'Коэффициент рекомендуемой стоимости клика (Q)', [
		validators.Required(message=u'Введите Q'),
		validators.NumberRange(min=1.0, message=u'Такой коэффициент недопустим')
	])
	m = DecimalField(u'Минимальная комиссия с одного клика (M)', [
		validators.Required(message=u'Введите M'),
		validators.NumberRange(min=0.0, message=u'Такая комиссия недопустима')
	], description=u'C &ge; D + M')
	mail = BooleanField(u'Письмо пользователю', default=False)
	
	
class GamakAppForm(Form):
	name = TextField(u'Название приложения', [
		validators.Required(message = (u'Введите название приложения'))
	])
	url = TextField(u'URL', [
		validators.Required(message = u'Введите URL приложения'),
		validators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	developer = TextField(u'Разработчик', [
		validators.Required(message = (u'Введите разработчика приложения'))
	])
	desc = TextAreaField(u'Описание приложения', [
		validators.Required(message = (u'Введите описание приложения')),
		validators.Length(min=1, max=500, message=(u'Описание должно быть длиной не более 500 символов'))
	])
	image = myfields.ImageField(u'Выберите изображение', [
		validators.FileRequired(message=u'Выберите изображение на диске'),
		validators.FileFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	], description=u'Форматы: JPG (JPEG), GIF, PNG')
	active = BooleanField(u'Активно', default=True)

class GamakAppEditForm(GamakAppForm):
	image = myfields.ImageField(u'Выберите изображение', [
		validators.FileFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	], description=u'Форматы: JPG (JPEG), GIF, PNG')


