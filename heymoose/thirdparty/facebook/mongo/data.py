from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.fields import NumberField
from heymoose import mg
from mongoalchemy.document import Index
from datetime import datetime
from pymongo import Connection
import gridfs

class GridfsField(mg.Field):
	def __init__(self, **kwargs):
		super(GridfsField, self).__init__(**kwargs)

		self.db = Connection().gridfs_data
		self.fs = gridfs.GridFS(self.db)

	#edit binary data not implemented, we simply delete and writ enew data
	#it is not bottleneck, because we are not going to edit gifts very often
	def flush_data(self, data):
		if not getattr(self, 'current_file_id', False):
			print "Write new data"
			return self.fs.put(data)
		else:
			print "Delete before write new data"
			self.fs.delete(getattr(self,'current_file_id'))
			return self.fs.put(data)
		
	def wrap(self, value):
		return self.flush_data(value)

	def unwrap(self, value):
		data = self.fs.get(value)
		if data:
			self.current_file_id = value
			return data.read()
		else:
			return None

	def validate_wrap(self, value):
		pass

class Performer(mg.Document):
	user_id_index = Index().ascending('user_id').unique()

	user_id = mg.StringField()
	oauth_token = mg.StringField()
	expires = mg.StringField()
	dirty = mg.BoolField(default=False)
	fullname = mg.StringField()
	firstname = mg.StringField()
	lastname = mg.StringField()
	offers_count = mg.IntField(default=0)
	date = mg.DateTimeField(default=datetime.now())
	
class Gifts(mg.Document):
	title = mg.StringField()
	price = mg.IntField()
	desc = mg.StringField()
	data = GridfsField()
	date = mg.DateTimeField(default=datetime.now())

class Invitations(mg.Document):
	from_id_index = Index().ascending('from_id').unique()
	from_id_index.ascending('to_id').unique()

	from_id = mg.StringField()
	to_id = mg.StringField()
	date = mg.DateTimeField(default=datetime.now())

class AccountAction(mg.Document):
	version_id_index = Index().ascending('version').unique()
	version_id_index.ascending('performer_id').unique()
	
	version = mg.IntField(default=0)
	balance = mg.IntField(default=0)
	performer_id = mg.StringField()

	recipient_id = mg.StringField(default="")
	gift_id = mg.StringField(default="")

	offer_id = mg.StringField(default="")
	
	operation = mg.EnumField(mg.StringField(), 'gift', 'offer', 'mlm')
	date = mg.DateTimeField(default=datetime.now())


import unittest
if __name__ == "__main__":
	class PerformerTest(unittest.TestCase):
		def test_user_creation(self):
			user = Performer(user_id="12321321321",
								oauth_token="qweqweqweqwe",
								expires=123,
								fullname="",
								firstname="",
								lastname="")
			user.save()

		def test_send_gift(self):
			for i in range(10):
				action = AccountAction(version=i,
										amount=10,
										performer_id="12321321321",
										operation="gift")
				action.save()
		def test_account_actions(self):
			action = AccountAction.query.filter(AccountAction.performer_id == "12321321321").descending('version').first()
			print action.version
	unittest.main()
