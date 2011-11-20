# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, validators, PasswordField, IntegerField, TextAreaField, DecimalField, RadioField, SelectField, FileField
import heymoose.core.actions.roles as roles

class LoginForm(Form):
	username = TextField('username', [
						 validators.Length(min=4, max=25, message = ('Некорректное имя пользователя')),
						 validators.Required(message = ('Введите имя пользователя'))])
	password = PasswordField('password', [
							 validators.Length(min=4, max=16, message = ('Некорректный пароль')),
							 validators.Required(message = ('Введите пароль'))])

class RoleForm(Form):
	role = SelectField('role', choices=[(roles.DEVELOPER, roles.DEVELOPER),
										(roles.CUSTOMER, roles.CUSTOMER)])

class RegisterForm(Form):
	username = TextField('username', [
						 validators.Length(min=4, max=25, message = ('Некорректное имя пользователя')),
						 validators.Required(message = ('Введите имя пользователя'))])
	email = TextField('Email Address', [
						validators.Email("Некорректный email адресс"),
						validators.Required(message = ('Введите email адресс'))])

	password = PasswordField('password', [
							 validators.Length(min=4, max=16, message = ('Длинна пароля должна быть от 4 до 16 символов')),
							 validators.Required(message = ('Введите пароль'))])

	password2 = PasswordField('password2', [
							 validators.Length(min=4, max=16, message = ('Длинна пароля должна быть от 4 до 16 символов')),
							 validators.Required(message = ('Введенные пароли не совпадают'))])
	role = SelectField('role', choices=[(roles.DEVELOPER, roles.DEVELOPER),
										(roles.CUSTOMER, roles.CUSTOMER)])
	captcha = TextField('captcha', [])

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
	ordername = TextField('ordername', [validators.Length(min=1, max=50, message=('Название заказа должно быть от 1 до 50 симолов')),
						  				validators.Required(message = ('Введите название заказа'))])
	orderdesc = TextAreaField('orederdesc', [validators.Length(min=1, max=200, message=('Описание заказа должно быть от 1 до 200 символов')),
											validators.Required(message = ('Введите описание'))])
	orderbody = TextField('orederbody', [validators.Required(message = ('Введите тело'))])
	orderbalance = IntegerField('orderbalance', [validators.Required(message = ('Укажите баланс для заказа')),
						validators.NumberRange(min=1, max=3000000, message=('Допустимый баланс от 1 до 3000000 рублей'))])
	ordercpa = IntegerField('oredercpa', [validators.Required(message = ('Введите cpa'))])
	orderautoaprove = BooleanField('orderautoaprove', default=False)
	orderallownegativebalance = BooleanField('orderallownegativebalance', default=False)
	ordermale = SelectField('ordermale', choices=[('True','male'),('False','female'),('None','all')])
	orderminage = IntegerField('orderminage', [validators.NumberRange(min=1, max=170, message=('Допустимый возраст: от 1 до 170 лет'))])
	ordermaxage = IntegerField('ordermaxage', [validators.NumberRange(min=1, max=170, message=('Допустимый возраст: от 1 до 170 лет'))])
	
class AppForm(Form):
	appcallback = TextField('appcallback', [validators.Required(message = ('Введите callback'))])
	appurl = TextField('appurl', [validators.Required(message = ('Введите appurl для возврата в ваше приложение'))])
	appplatform = SelectField('appplatform', choices=[('VKONTAKTE','VKONTAKTE'),('FACEBOOK','FACEBOOK'),('ODNOKLASSNIKI','ODNOKLASSNIKI')])
	
class BalanceForm(Form):
	amount = IntegerField('orderbalance', [validators.Required(message = ('Укажите баланс')),
						validators.NumberRange(min=1, max=3000000, message=('Допустимый баланс от 1 до 3000000 рублей'))])


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
