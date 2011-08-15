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
from connection import connection
import random
import string
import hashlib

class BaseModel(object):
	def __init__(self, error=None):
		pass

	@classmethod
	def execute(cls, query, args):
		connection.execute_query(query, args)

	def query_one(self, query, args):
		res = connection.select_query(query, args)
		return res

	def query_all(self, query, args):
		res = connection.select_query(query, args)
		return res

	@classmethod
	def query(cls, query, args, one=False):
		res = connection.select_query(query, args, one)
		return res

	@classmethod
	def get(cls, limit = 10, offset = 0, **kwargs):
		if not getattr(cls, 'table_name', None):
			raise Exception("from @classmethod get, table_name not defined for " + str(cls))

		if not getattr(cls, 'create_object', None):
			raise Exception("from @classmethod get, create_object not implemented for " + str(cls))

		query = "SELECT * FROM " + str(cls.table_name)
		ln = len(kwargs)
		if ln:
			query += " WHERE "
			j = 1
			for i in kwargs.iteritems():
				query += str(i[0]) + "=%(" + str(i[0]) + ")s"
				if j < ln:
					query += " AND "
				j += 1
		query += " LIMIT %d, %d " %(offset, limit)

		res = cls.query(query, kwargs)
		if not res:
			return []

		lst = []
		for item in res:
			o = cls.create_object(item)
			lst.append(o)
		return lst


class User(BaseModel):
	table_name = 'users'
	def __init__(self, username, email, passwordhash):
		super(User, self).__init__()
		self._username = username
		self._email = email
		self._passwordhash = passwordhash
		self._userid = None

	def __str__(self):
		res = str(self._username) + " " + str(self._email) + " " + str(self._passwordhash) + " " + str(self._userid)
		return res

	@classmethod
	def get_user_byid(cls, user_id):
		args = {'id' : user_id}
		query = "SELECT * FROM " + User.table_name + " WHERE id = %(id)s"
		res = cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		else:
			return None

	@classmethod
	def get_user(cls, username):
		args = {'name' : username.encode('utf8')}
		query = "SELECT * FROM " + User.table_name + " WHERE name = %(name)s"
		res =cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		else:
			return None

	@classmethod
	def check_user(cls, email):
		args = {'email':email.encode('utf8')}
		query = "SELECT * FROM " + User.table_name + " WHERE email = %(email)s"
		res =cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		else:
			return None

	def save(self):
		args = {'name': self._username.encode('utf8'),
				'email' : self._email.encode('utf8'),
				'password' : self._passwordhash}
		query = "SELECT merge_user(%(email)s, %(name)s, %(password)s)"
		self.execute(query, args)

	@classmethod
	def create_object(cls, item):
		user = cls(item['name'].decode('utf8'),
				   item['email'].decode('utf8'),
				   item['password'])
		user._userid = item['id']
		return user

	@property
	def username(self):
		return self._username
	@username.setter
	def username(self, value):
		self._username = value

	@property
	def passwordhash(self):
		return self._passwordhash
	@passwordhash.setter
	def passwordhash(self, value):
		self._passwordhash = value

	@property
	def email(self):
		return self._email
	@email.setter
	def email(self, value):
		self._email = value

	@property
	def userid(self):
		return self._userid

class Captcha(BaseModel):
	table_name = 'captcha'
	def __init__(self, q_id, question, answer):
		super(Captcha, self).__init__()
		self._question = question
		self._answer = answer
		self._qid = q_id

	@classmethod
	def check_captcha(cls, q_id, answer):
		args = {'id':q_id}
		query = "SELECT * FROM " + cls.table_name + " WHERE id = %(id)s"
		res =cls.query(query, args, one=True)
		if res:
			captcha = cls.create_object(res)
			if captcha.answer != answer:
				return None
			return captcha
		else:
			return None

	@classmethod
	def get_random(cls, min=1, max=1000):
		r_id = random.randint(min, max)
		args = {'id':r_id}
		query = "SELECT * FROM " + cls.table_name + " WHERE id = %(id)s"
		res =cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		else:
			return None


	@classmethod
	def create_object(cls, item):
		captcha = cls(item['id'],
					  item['question'].decode('utf8'),
					  item['answer'].decode('utf8'))
		return captcha

	@property
	def qid(self):
		return self._qid

	@property
	def question(self):
		return self._question

	@property
	def answer(self):
		return self._answer

class Developer(BaseModel):
	table_name = "developers"
	def __init__(self, id, app_id=None, secret_key=None):
		super(Developer, self).__init__()
		self._id = id

		if not app_id:
			self._app_id = self.generate_app_id()
		else:
			self._app_id = app_id

		if not secret_key:
			self._secret_key = self.generate_secret_key()
		else:
			self._secret_key = secret_key

	def save(self):
		args = {'id': self._id,
				'app_id' : str(self._app_id),
				'secret_key' : str(self._secret_key)}
		query = "SELECT merge_developer(%(id)s, %(app_id)s, %(secret_key)s)"
		self.execute(query, args)


	def generate_app_id(self):
		random.seed()
		return int(random.random() * 10000000)

	def generate_secret_key(self):
		random.seed()
		d = [random.choice(string.letters + string.digits) for x in xrange(128)]
		s = "".join(d)
		return s

	def check_sign(self, sig):
		md5_hash = hashlib.md5()
		md5_hash.update(str(self.app_id) + self.secret_key)
		if str(md5_hash.hexdigest()) != str(sig):
			return False

		return True

	@classmethod
	def get_by_app_id(cls, app_id):
		args = {'app_id': str(app_id)}
		query = "SELECT * FROM " + cls.table_name + " WHERE app_id=%(app_id)s"
		res = cls.query(query, args, one=True)
		if not res:
			return None

		return cls.create_object(res)

	@classmethod
	def get_vkontakte_app_developer(cls, name='app_user'):
		args = {'name' : name}
		query = "SELECT * FROM " + cls.table_name + " WHERE id = (SELECT id FROM " + User.table_name + " WHERE name=%(name)s)"
		res = cls.query(query, args, one=True)
		if not res:
			return None

		return cls.create_object(res)

	@classmethod
	def get_developer(cls, id):
		args = {'id': id}
		query = "SELECT * FROM " + cls.table_name + " WHERE id=%(id)s"
		res = cls.query(query, args, one=True)
		if not res:
			return None

		return cls.create_object(res)


	@classmethod
	def create_object(cls, item):
		developer = cls(item['id'], item['app_id'], item['secret_key'])
		return developer


	@property
	def id(self):
		return self._id

	@property
	def app_id(self):
		return self._app_id

	@property
	def secret_key(self):
		return self._secret_key

class Order(BaseModel):
	table_name = "orders"
	def __init__(self, owner_id, title, balance, body, date=None, id=None):
		super(Order, self).__init__()
		self._owner_id = owner_id
		self._title = title
		self._balance = balance
		self._body = body
		self._id = id
		if date:
			self._date = date

	def save_new(self):
		args = {'owner_id': self._owner_id,
				'title' : self._title.encode('utf8'),
				'balance' : self._balance,
				'body' : self._body.encode('utf8')}
		query = "INSERT INTO " + self.table_name + " (owner_id, balance, title, body, date) VALUES(%(owner_id)s, %(balance)s, %(title)s, %(body)s, now())"
		self.execute(query, args)

	def save(self, id):
		args = {'id': id,
				'owner_id': self._owner_id,
				'title' : self._title.encode('utf8'),
				'balance' : self._balance,
				'body' : self._body.encode('utf8')}
		query = "UPDATE " + self.table_name + " SET owner_id = %(owner_id)s, title=%(title)s, balance=%(balance)s, body=%(body)s WHERE id=%(id)s"
		self.execute(query, args)
		return True

	@classmethod
	def delete_order(cls, order_id):
		args = {'id': order_id}
		query = "DELETE FROM " + cls.table_name + " WHERE id=%(id)s"
		cls.execute(query, args)

	@classmethod
	def load_orders(cls, owner_id, offset, limit=10):
		args = {'owner_id':owner_id,
				'offset': offset,
				'limit': limit}
		query = "SELECT * FROM " + cls.table_name + " WHERE owner_id = %(owner_id)s ORDER BY date LIMIT %(limit)s OFFSET %(offset)s"
		res = cls.query(query, args)
		lst = []
		if res:
			for next in res:
				lst.append(cls.create_object(next))
			return lst

		return None


	@classmethod
	def load_order(cls, owner_id, order_id):
		args = {'order_id': order_id,
				'owner_id': owner_id}
		query = "SELECT * FROM " +  cls.table_name + " WHERE owner_id=%(owner_id)s and id=%(order_id)s"
		res = cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)

		return None


	@classmethod
	def create_object(cls, item):
		order = cls(item['owner_id'],
					item['title'].decode('utf8'),
					item['balance'],
					item['body'].decode('utf8'),
					item['date'],
					item['id'])
		return order

	@property
	def id(self):
		return self._id

	@property
	def owner_id(self):
		return self._owner_id

	@property
	def title(self):
		return self._title

	@property
	def balance(self):
		return self._balance

	@property
	def body(self):
		return self._body

	@property
	def date(self):
		return self._date

class Category(BaseModel):
	table_name = "blog_category"
	def __init__(self, title):
		super(Category, self).__init__()
		self._title = title

	def save_new(self):
		args = {'title' : self._title.encode('utf8')}
		query = "INSERT INTO " + self.table_name + " (title) VALUES(%(title)s)"
		self.execute(query, args)

	@property
	def title(self):
		return self._title
	@property
	def id(self):
		return self._id

	@classmethod
	def create_object(cls, item):
		category = cls(item['title'].decode('utf8'))
		category._id = item['id']
		return category

	@classmethod
	def load_category(cls, cat_id):
		args = {'id' : str(cat_id)}
		query = "SELECT * FROM " + cls.table_name + " WHERE id=%(id)s"

		res = cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		return None

	@classmethod
	def load_categories(cls):
		query = "SELECT * FROM " + cls.table_name + " "
		res = cls.query(query, None)
		lst = []
		if res:
			for next in res:
				lst.append(cls.create_object(next))
			return lst

		return None

class Blog(BaseModel):
	table_name = "blog_records"
	def __init__(self, category_id, title, body, annotation, image_path=None, date=None):
		super(Blog, self).__init__()
		self._category_id = category_id
		self._title = title
		self._body = body
		self._image_path = image_path
		self._date = date
		self._annotation = annotation

	@classmethod
	def create_object(cls, item):
		image_path = None
		if item['image_path']:
			image_path = item['image_path'].decode('utf8');
		blog = cls(category_id = item['category_id'],
					title = item['title'].decode('utf8'),
					body = item['body'].decode('utf8'),
					annotation = item['annotation'].decode('utf8'),
					image_path=image_path,
					date = item['date'])
		blog._id = item['id']
		return blog

	@classmethod
	def load_blog_by_id(cls, blog_id):
		args = {"id": blog_id}
		query = "SELECT * FROM " + cls.table_name + " WHERE id=%(id)s"
		res = cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)

		return None

	@classmethod
	def load_blogs(cls, offset, limit=10):
		args = {"offset": offset,
				"limit" : limit}
		query = "SELECT * FROM " + cls.table_name + " ORDER BY date LIMIT %(limit)s OFFSET %(offset)s"
		res = cls.query(query, args)
		lst = []
		if res:
			for next in res:
				lst.append(cls.create_object(next))
			return lst

		return None

	@classmethod
	def load_blogs_by_category(cls, category_id, offset, limit=10):
		args = {'category_id' : category_id,
				'offset' : offset,
				'limit' : limit}
		query = "SELECT * FROM " + cls.table_name + " WHERE category_id=%(category_id)s ORDER BY DATE LIMIT %(limit)s OFFSET %(offset)s"
		res = cls.query(query, args)
		lst = []
		if res:
			for next in res:
				lst.append(cls.create_object(next))
			return lst

		return None

	def save(self):
		args = {'category_id' : str(self._category_id),
				'title' : self._title.encode('utf8'),
				'body' : self._body.encode('utf8'),
				'annotation' : self._annotation.encode('utf8'),
				'id' : self._id}
		if self._image_path:
			args['image_path'] = self._image_path.encode('utf8')
			query = "UPDATE " + self.table_name + " SET category_id = %(category_id)s, title = %(title)s, body = %(body)s, annotation = %(annotation)s, image_path = %(image_path)s, date = now() WHERE id=%(id)s"
		else:
			print "UPDATE blog with id = " + str(self._id)
			query = "UPDATE " + self.table_name + " SET category_id = %(category_id)s, title = %(title)s, body = %(body)s, annotation = %(annotation)s, date = now() WHERE id=%(id)s"

		self.execute(query, args)

	def save_new(self):
		args = {'category_id' : str(self._category_id),
				'title' : self._title.encode('utf8'),
				'body' : self._body.encode('utf8'),
				'annotation' : self._annotation.encode('utf8')}
		if self._image_path:
			args['image_path'] = self._image_path.encode('utf8')
			query = "INSERT INTO " + self.table_name + " (category_id, title, body, annotation, image_path, date) VALUES(%(category_id)s, %(title)s, %(body)s, %(annotation)s, %(image_path)s, now())"
		else:
			query = "INSERT INTO " + self.table_name + " (category_id, title, body, annotation, date) VALUES(%(category_id)s, %(title)s, %(body)s, %(annotation)s, now())"

		self.execute(query, args)

	@property
	def id(self):
		return self._id

	@property
	def category_id(self):
		return self._category_id
	@category_id.setter
	def category_id(self, value):
		self._category_id = value

	@property
	def annotation(self):
		return self._annotation
	@annotation.setter
	def annotation(self, value):
		self._annotation = value

	@property
	def title(self):
		return self._title
	@title.setter
	def title(self, value):
		self._title = value

	@property
	def body(self):
		return self._body
	@body.setter
	def body(self, value):
		self._body = value


	@property
	def image_path(self):
		return self._image_path
	@image_path.setter
	def image_path(self, value):
		self._image_path = value

	@property
	def date(self):
		return self._date

class FeedBack(BaseModel):
	table_name = "feedback"
	def __init__(self, email, comment):
		super(FeedBack, self).__init__()
		self._email = email
		self._comment = comment

	def save_new(self):
		args = {'email' : self._email.encode('utf8'),
				'body' : self._comment.encode('utf8')}
		query = "INSERT INTO " + self.table_name + " (email, body) VALUES(%(email)s, %(body)s)"
		self.execute(query, args)

	@classmethod
	def create_object(cls, item):
		feedback = cls(email = item['email'].decode('utf8'),
					comment = item['body'].decode('utf8'))
		feedback._id = item['id']
		return feedback

	@property
	def email(self):
		return self._email
	@property
	def comment(self):
		return self._email

class Offer(BaseModel):
	table_name = "offers"
	table_stat = "offers_in_action"
	def __init__(self, title, body, url, time, voice):
		super(Offer, self).__init__()
		self._title = title
		self._body = body
		self._url = url
		self._time = time
		self._voice = voice

	def save(self):
		args = {'title' : self._title.encode('utf8'),
				'body' : self._body.encode('utf8'),
				'url' : self._url.encode('utf8'),
				'time' : self._time.encode('utf8'),
				'voice' : self._voice.encode('utf8')}
		query = "INSERT INTO " + self.table_name + " (title, body, url, time, voice, date) VALUES(%(title)s, %(body)s, %(url)s, %(time)s, %(voice)s, now())"
		self.execute(query, args)
		return True

	@classmethod
	def get_offer_by_id(cls, offer_id):
		args = {'id' : offer_id}
		query = "SELECT * FROM " + cls.table_name + " WHERE id=%(id)s"
		res = cls.query(query, args, one=True)
		if res:
			return cls.create_object(res)
		return None

	@classmethod
	def isOfferAvailable(cls, user_id, offer_id):
		args = {'offer_id' : offer_id,
				'user_id' : user_id}
		query = "SELECT * FROM " + cls.table_stat + " WHERE offer_id=%(offer_id)s AND user_id=%(user_id)s"
		res = cls.query(query, args, one=True)
		if res:
			return False
		return True

	@classmethod
	def create_object(cls, item):
		offer = cls(item['title'].decode('utf8'),
					item['body'].decode('utf8'),
					item['url'].decode('utf8'),
					item['time'],
					item['voice'])

		offer._id = item['id']
		return offer

	def save_stat(self, user_id, app_id, voice_count, status):
		args = {'offer_id': self.id,
				'user_id' : user_id,
				'app_id' : app_id,
				'voice_count' : voice_count,
				'status' : status}

		query = "INSERT INTO " + self.table_stat + " (offer_id, user_id, app_id, voice_count, status, date) VALUES(%(offer_id)s, %(user_id)s, %(app_id)s, %(voice_count)s, %(status)s, now())"
		self.execute(query, args)
		return True

	@property
	def id(self):
		return self._id
	@property
	def title(self):
		return self._title
	@property
	def body(self):
		return self._body
	@property
	def url(self):
		return self._url
	@property
	def time(self):
		return self._time
	@property
	def voice(self):
		return self._voice

class OfferFormer(BaseModel):
	table_name = "offers_by_dev"
	offers_table_name = "offers"
	def __init__(self):
		super(OfferFormer, self).__init__()

	@classmethod
	def get_offer_form(cls):
		args = {'limit' : 10,
				'offset' : 0}
		query = "SELECT * FROM " + cls.offers_table_name + " ORDER BY DATE LIMIT %(limit)s OFFSET %(offset)s"
		res = cls.query(query, args)
		lst = []
		if res:
			for next in res:
				lst.append(Offer.create_object(next))
			return lst

		return None
