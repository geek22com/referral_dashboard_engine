# -*- coding: utf-8 -*-
from wtforms import Form, validators, BooleanField, TextField, PasswordField, \
	IntegerField, DecimalField, TextAreaField, SelectField, HiddenField
from wtforms.fields import Label
from heymoose.core import actions
from heymoose.core.actions import roles
import validators as myvalidators
import fields as myfields
import random, hashlib


class CaptchaForm(Form):
	captcha = TextField(u'', [validators.Required(message=u'Введите число')])
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

class RoleForm(Form):
	role = SelectField('role', choices=[(roles.DEVELOPER, roles.DEVELOPER),
										(roles.CUSTOMER, roles.CUSTOMER)])


class RegisterForm(Form):
	username = TextField(u'Имя пользователя (ник)', [
		 validators.Length(min=4, max=25, message = u'Некорректное имя пользователя'),
		 validators.Required(message = u'Введите имя пользователя')
	])
	email = TextField(u'E-mail', [
		validators.Email(message = u'Некорректный email адрес'),
		validators.Required(message = u'Введите email адрес'),
		myvalidators.check_email_not_registered
	])
	password = PasswordField(u'Пароль', [
		validators.Length(min=4, max=16, message = u'Длина пароля должна быть от 4 до 16 символов'),
		validators.Required(message = u'Введите пароль')
	])
	password2 = PasswordField(u'Повторите пароль', [
		validators.Length(min=4, max=16, message = u'Длина пароля должна быть от 4 до 16 символов'),
		validators.EqualTo('password', message = u'Введенные пароли не совпадают'),
		validators.Required(message = u'Введите пароль повторно')
	])
	
class DeveloperRegisterForm(RegisterForm):
	invite = TextAreaField(u'Код приглашения', [
		validators.Required(message=u'Скопируйте сюда полученный код приглашения'),
		myvalidators.check_invite
	])
	
class CustomerRegisterForm(RegisterForm):
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
		myvalidators.check_password
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
	comment = TextAreaField(u'Вопрос или сообщение')


class OrderForm(Form):
	ordername = TextField(u'Название', [
		validators.Length(min=1, max=50, message=(u'Название заказа должно быть от 1 до 50 символов')),
		validators.Required(message = (u'Введите название заказа'))
	])
	orderurl = TextField(u'URL', [
		validators.Required(message = (u'Введите URL')),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	orderbalance = DecimalField(u'Баланс', [
		validators.Required(message = (u'Укажите баланс для заказа')),
		validators.NumberRange(min=1, max=3000000, message=(u'Такой баланс недопустим'))
	])
	ordercpa = DecimalField(u'Стоимость действия (CPA)', [validators.Required(message = (u'Введите CPA'))])
	orderautoapprove = BooleanField(u'Автоподтверждение', default=False)
	orderreentrant = BooleanField(u'Многократное прохождение', default=False)
	orderallownegativebalance = BooleanField(u'Разрешить кредит', default=True)
	ordermale = SelectField(u'Пол', choices=[(u'True', u'мужской'), (u'False', u'женский'), (u'', u'любой')], default='')
	orderminage = myfields.NullableIntegerField(u'Минимальный возраст', [
		myvalidators.NumberRangeEx(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))
	])
	ordermaxage = myfields.NullableIntegerField(u'Максимальный возраст', [
		myvalidators.NumberRangeEx(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))
	])
	ordercitiesfilter = SelectField(u'Фильтр по городам', default=u'', choices=[
		(u'', u'не учитывать'),
		(u'INCLUSIVE', u'только указанные'),
		(u'EXCLUSIVE', u'все, кроме указанных')
	])
	ordercities = TextField(u'Список городов')
	
class RegularOrderForm(OrderForm):
	orderdesc = TextAreaField(u'Описание', [
		validators.Length(min=1, max=200, message=(u'Описание заказа должно быть от 1 до 200 символов')),
		validators.Required(message = (u'Введите описание'))
	])
	orderimage = myfields.ImageField(u'Выберите изображение', [
		myvalidators.FileRequired(message=u'Выберите изображение на диске'),
		myvalidators.ImageFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	])

class BannerOrderForm(OrderForm):
	orderbannersize = SelectField(u'Размер баннера', coerce=int)
	orderimage = myfields.ImageField(u'Выберите изображение', [
		myvalidators.FileRequired(message=u'Выберите изображение на диске'),
		myvalidators.ImageFormat(message=u'Выберите изображение в формате JPG, GIF или PNG')
	])
	
	def validate_orderimage(self, field):
		if field.data is None: return
		size = actions.bannersizes.get_banner_size(self.orderbannersize.data)
		if field.data.size[0] != size.width or field.data.size[1] != size.height:
			raise ValueError(u'Размер изображения должен совпадать с указанным')
		
class VideoOrderForm(OrderForm):
	ordervideourl = TextField(u'URL видеозаписи', [
		validators.Required(message = (u'Введите URL')),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	
	
class BannerSizeForm(Form):
	width = IntegerField(u'Ширина', [
		validators.Required(message=u'Укажите ширину баннера'),
		validators.NumberRange(min=1, max=3000, message=u'Баннер может иметь ширину от 1 до 3000 пикселей')
	])
	height = IntegerField(u'Высота', [
		validators.Required(message=u'Укажите высоту баннера'),
		validators.NumberRange(min=1, max=3000, message=u'Баннер может иметь высоту от 1 до 3000 пикселей')
	])
	
	
class AppForm(Form):
	apptitle = TextField(u'Название', [
		validators.Length(min=1, max=100, message=(u'Название приложения должно иметь длину от 1 до 100 символов')),
		validators.Required(message = (u'Введите название приложения'))
	])
	appcallback = TextField(u'Callback', [
		validators.Required(message = u'Введите callback для вашего приложения'),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	appurl = TextField(u'URL', [
		validators.Required(message = u'Введите URL для возврата в ваше приложение'),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	appplatform = SelectField(u'Платформа', choices=[
		('VKONTAKTE', u'ВКонтакте'),
		('FACEBOOK', u'Facebook'),
		('ODNOKLASSNIKI', u'Одноклассники')
	])
	
class BalanceForm(Form):
	amount = IntegerField(u'Сумма пополнения', [
		validators.Required(message = u'Укажите баланс'),
		validators.NumberRange(min=1, max=3000000, message=u'Допустимый баланс от 1 до 3000000 рублей')
	])


class GiftForm(Form):
	to_id = TextField('to_id', [validators.Required()])
	gift_id = TextField('gift_id', [validators.Required()])
	message = TextField('message')

class GiftAddForm(Form):
	gifttitle = TextField('gifttitle', [validators.Required()])
	giftprice = TextField('giftprice', [validators.Required()])
	giftdesc = TextField('giftdesc', [validators.Required()])

class FacebookHelpForm(Form):
	email = TextField('Email Address', [
						validators.Email(u"Некорректный email"),
						validators.Required(message = (u'Введите email'))])
	comment = TextAreaField('Comment', [validators.Required(message = (u'Напишите сообщение') )])

class OfferForm(Form):
	app_id = IntegerField('app_id', [validators.Required(),
						validators.NumberRange(min=1, max=4000000000)])
	sig = TextField('sig', [validators.Required()])
	error_url = TextField('error_url', [validators.Optional()])
	offer_id = IntegerField('offer_id', [validators.Optional(),
										validators.NumberRange(min=1, max=4000000000)])
	user_id = IntegerField('user_id', [validators.Optional(),
										validators.NumberRange(min=0)])
