# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, validators, PasswordField, IntegerField, TextAreaField, SelectField, FileField
import heymoose.core.actions.roles as roles
import validators as myvalidators
import fields as myfields

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

class ContactForm(Form):
	name = TextField('contactname')
	email = TextField('contactemail', [
					  validators.Email("Некорректный email адресс")])
	phone = TextField('contactphone', [
					  validators.Required("Введите ваш номер телефона, чтобы мы могли позвонить вам.")])
	comment = TextAreaField('contactcomment')
	captcha_answer = TextField('captcha_answer', [validators.Required(message = ('Введите каптчу'))])


class OrderForm(Form):
	ordername = TextField(u'Название', [
		validators.Length(min=1, max=50, message=(u'Название заказа должно быть от 1 до 50 символов')),
		validators.Required(message = (u'Введите название заказа'))
	])
	orderurl = TextField(u'URL', [
		validators.Required(message = (u'Введите URL')),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
	])
	orderbalance = IntegerField(u'Баланс', [
		validators.Required(message = (u'Укажите баланс для заказа')),
		validators.NumberRange(min=1, max=3000000, message=(u'Такой баланс недопустим'))
	])
	ordercpa = IntegerField(u'Стоимость действия (CPA)', [validators.Required(message = (u'Введите CPA'))])
	orderautoapprove = BooleanField(u'Автоподтверждение', default=False)
	orderreentrant = BooleanField(u'Многократное прохождение', default=False)
	orderallownegativebalance = BooleanField(u'Разрешить кредит', default=True)
	ordermale = SelectField(u'Пол', choices=[(u'True', u'мужской'), (u'False', u'женский'), (u'', u'любой')], default='')
	orderminage = myfields.NullableIntegerField(u'Минимальный возраст', [myvalidators.NumberRangeEx(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))])
	ordermaxage = myfields.NullableIntegerField(u'Максимальный возраст', [myvalidators.NumberRangeEx(min=1, max=170, message=(u'Допустимый возраст: от 1 до 170 лет'))])
	
class RegularOrderForm(OrderForm):
	orderdesc = TextAreaField(u'Описание', [
		validators.Length(min=1, max=200, message=(u'Описание заказа должно быть от 1 до 200 символов')),
		validators.Required(message = (u'Введите описание'))
	])
	orderimage = FileField(u'Выберите изображение', [myvalidators.FileRequired(message=u'Выберите изображение на диске')])

class BannerOrderForm(OrderForm):
	orderimage = FileField(u'Выберите изображение', [
		myvalidators.FileRequired(message=u'Выберите изображение на диске')
	])
	
class VideoOrderForm(OrderForm):
	ordervideourl = TextField(u'URL видеозаписи', [
		validators.Required(message = (u'Введите URL')),
		myvalidators.URLWithParams(message = u'Введите URL в формате http://*.*')
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
