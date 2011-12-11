# -*- coding: utf-8 -*-
# Напишу это здесь, ибо это выносит мозг лично мне
# В формах данные (благодаря WTForm) приходят уже в unicode, поэтому
# Если сделать данные.decode('utf8'), то вылязит exception UnicodeEncodeError: 'ascii' codec can't encode character...
# Например: u"\u0411".decode("utf-8") - это вызовит exception
# Подробно тут: http://wiki.python.org/moin/UnicodeEncodeError
# В идеале осознать: http://docs.python.org/howto/unicode.html
# Остановимся на том что данные в модель будем передовать уже в юникод.
# То есть:
#	1. На входе в модель кто-то должен делать данные.decode()
#	2. При сохранении в базу модель САМА делает данные.encode()
#	3. При чтении из базы модель САМА делает данные.decode()
#
from heymoose import mg as mongo
from mongoalchemy.document import Index
from datetime import datetime

class Captcha(mongo.Document):
	c_id_index = Index().ascending('c_id').unique()
	c_id = mongo.IntField()
	question = mongo.StringField()
	answer = mongo.StringField()

class Category(mongo.Document):
	title = mongo.StringField()

class Blog(mongo.Document):
	image_path = mongo.StringField()
	category_id = mongo.StringField()
	title = mongo.StringField()
	body = mongo.StringField()
	annotation = mongo.StringField()
	date = mongo.DateTimeField(default=datetime.now())

class Contact(mongo.Document):
	name = mongo.StringField()
	email = mongo.StringField()
	phone = mongo.StringField()
	desc = mongo.StringField()
	date = mongo.DateTimeField()
	read = mongo.BoolField(default=False)


class FeedBack(mongo.Document):
	email = mongo.StringField()
	body = mongo.StringField()
	date = mongo.DateTimeField(default=datetime.now())
	
	
class Invite(mongo.Document):
	code = mongo.StringField()
	registered = mongo.BoolField(default=False)
	created = mongo.DateTimeField()
