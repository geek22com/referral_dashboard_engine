# -*- coding: utf-8 -*-
from heymoose import app
from flaskext.mongoalchemy import MongoAlchemy, BaseQuery
from datetime import datetime
import os, mimetypes

mongo = MongoAlchemy(app)


class HeyMooseQuery(BaseQuery):
	def get_or_create(self, **kwargs):
		obj = self.filter_by(**kwargs).first()
		if not obj:
			obj = self.type(**kwargs)
		return obj


class Contact(mongo.Document):
	name = mongo.StringField()
	email = mongo.StringField()
	phone = mongo.StringField()
	desc = mongo.StringField()
	date = mongo.DateTimeField()
	read = mongo.BoolField(default=False)
	partner = mongo.BoolField(default=False, allow_none=True)


class UserInfo(mongo.Document):
	query_class = HeyMooseQuery
	
	user_id = mongo.IntField()
	city = mongo.StringField()


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


class AdminPermissions(mongo.Document):
	query_class = HeyMooseQuery
	user_id = mongo.IntField()
	groups = mongo.ListField(mongo.StringField(), default=[])
	_all_groups = app.config.get('ADMIN_GROUPS')

	def permissions(self):
		permissions = set()
		for group in self.groups:
			permissions |= self._all_groups.get(group, set())
