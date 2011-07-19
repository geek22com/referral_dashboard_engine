# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, validators, PasswordField, IntegerField, TextAreaField, DecimalField

class LoginForm(Form):
	username = TextField('username', [
						 validators.Length(min=4, max=25, message = ('Некорректное имя пользователя')),
						 validators.Required(message = ('Введите имя пользователя'))])
	password = PasswordField('password', [
							 validators.Length(min=4, max=16, message = ('Некорректный пароль')),
							 validators.Required(message = ('Введите пароль'))])

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
	orderquestions = TextAreaField('orederquestions', [validators.Required(message = ('Введите вопросы'))])

