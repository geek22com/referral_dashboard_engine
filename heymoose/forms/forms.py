# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, validators, PasswordField, IntegerField, TextAreaField, DecimalField, RadioField, SelectField
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
										(roles.CUSTOMER, roles.CUSTOMER),
										(roles.ADMIN, roles.ADMIN)])
	captcha = TextField('captcha', [])

class FeedBackForm(Form):
	email = TextField('Email Address', [
					  validators.Email("Некорректный email адресс")])
	comment = TextAreaField('Comment', [validators.Required(message = ('Напишите ваше пожелание') )])
	captcha = TextField('captcha', [])

class OrderForm(Form):
	ordername = TextField('ordername', [validators.Length(min=1, max=255, message=('Название заказа должна быть от 1 до 255 симолов')),
						  				validators.Required(message = ('Введите название заказа'))])
	orderbalance = IntegerField('orderbalance', [validators.Required(message = ('Укажите баланс для заказа')),
						validators.NumberRange(min=1, max=3000000, message=('Допустимый баланс от 1 до 3000000 рублей'))])
	orderbody = TextField('orederbody', [validators.Required(message = ('Введите тело'))])
	ordercpa = IntegerField('oredercpa', [validators.Required(message = ('Введите cpa'))])

class BalanceForm(Form):
	amount = IntegerField('orderbalance', [validators.Required(message = ('Укажите баланс')),
						validators.NumberRange(min=1, max=3000000, message=('Допустимый баланс от 1 до 3000000 рублей'))])


class GiftForm(Form):
	from_id = IntegerField('from_id', [validators.Required()])
	to_id = IntegerField('to_id', [validators.Required()])
	gift_id = TextField('gift_id', [validators.Required()])
	message = TextField('message')


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
