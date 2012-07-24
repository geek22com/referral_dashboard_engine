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
from heymoose import app
from heymoose import mg as mongo
from mongoalchemy.document import Index
from flaskext.mongoalchemy import BaseQuery
from datetime import datetime
import os, mimetypes

class HeyMooseQuery(BaseQuery):
	def get_or_create(self, **kwargs):
		obj = self.filter_by(**kwargs).first()
		if not obj:
			obj = self.type(**kwargs)
		return obj


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
	partner = mongo.BoolField(default=False, allow_none=True)


class FeedBack(mongo.Document):
	email = mongo.StringField()
	body = mongo.StringField()
	date = mongo.DateTimeField(default=datetime.now())
	
	
class Invite(mongo.Document):
	code = mongo.StringField()
	registered = mongo.BoolField(default=False)
	created = mongo.DateTimeField()

class UserInfo(mongo.Document):
	query_class = HeyMooseQuery
	
	user_id = mongo.IntField()
	block_date = mongo.DateTimeField()
	block_reason = mongo.StringField()

class OrderInfo(mongo.Document):
	query_class = HeyMooseQuery
	
	order_id = mongo.IntField()
	block_date = mongo.DateTimeField()
	block_reason = mongo.StringField()
	
class GamakApp(mongo.Document):
	name = mongo.StringField()
	url = mongo.StringField()
	developer = mongo.StringField()
	desc = mongo.StringField()
	mime_type = mongo.StringField()
	date = mongo.DateTimeField()
	active = mongo.BoolField(default=True)
	
	image_dir = 'gamak'
	
	def image_file(self):
		extension = mimetypes.guess_extension(self.mime_type)
		return os.path.join(self.image_dir, '{0}{1}'.format(self.mongo_id, extension))
	
	def image_path(self):
		return os.path.join(app.config.get('UPLOAD_PATH'), self.image_file())


class DummyAction(mongo.Document):
	query_class = HeyMooseQuery
	
	offer_id = mongo.IntField()
	date = mongo.DateTimeField()


class NewsItem(mongo.Document):
	title = mongo.StringField()
	summary = mongo.StringField()
	text = mongo.StringField()
	image = mongo.StringField(default='heymoose.png')
	date = mongo.DateTimeField()
	active = mongo.BoolField(default=True)
	on_main = mongo.BoolField(default=False)
	
	_images_dir = app.config.get('NEWS_IMAGES_DIR')
	
	@property
	def image_url(self):
		return os.path.join(self._images_dir, self.image or 'heymoose.png')


class Notification(mongo.Document):
	user_id = mongo.IntField()
	body = mongo.StringField()
	date = mongo.DateTimeField()
	read = mongo.BoolField(default=False)
	notified = mongo.BoolField(default=False)
