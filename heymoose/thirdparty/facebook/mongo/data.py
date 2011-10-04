from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.fields import NumberField
from heymoose import mg
from mongoalchemy.document import Index
from datetime import datetime

class Performer(mg.Document):
	user_id_index = Index().ascending('user_id').unique()

	user_id = mg.StringField()
	oauth_token = mg.StringField()
	expires = mg.StringField()
	dirty = mg.BoolField(default=False)
	fullname = mg.StringField()
	firstname = mg.StringField()
	lastname = mg.StringField()

class Gifts(mg.Document):
	title = mg.StringField()
	price = mg.IntField()
	desc = mg.StringField()
	path = mg.StringField()

class AccountAction(mg.Document):
	version_id_index = Index().ascending('version').unique()
	version_id_index.ascending('performer_id').unique()
	
	version = mg.IntField(default=0)
	balance = mg.IntField(default=0)
	performer_id = mg.StringField()

	recipient_id = mg.StringField(default="")
	gift_id = mg.StringField(default="")

	offer_id = mg.StringField(default="")
	
	operation = mg.EnumField(mg.StringField(), 'gift', 'offer')
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
