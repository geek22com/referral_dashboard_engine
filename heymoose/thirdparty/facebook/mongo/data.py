from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.fields import NumberField
from heymoose import mg
from mongoalchemy.document import Index
from datetime import datetime

class Performer(mg.Document):
	user_id_index = Index().ascending('user_id').unique()

	amount = mg.IntField(default=0)
	donations = mg.ListField(mg.DictField(mg.StringField()), default=None) # We don't use separate collection,
																		# because mongo support transaction only for single collection

	user_id = mg.StringField()
	oauth_token = mg.StringField()
	expires = mg.IntField()
	dirty = mg.BoolField(default=False)
	fullname = mg.StringField()
	firstname = mg.StringField()
	lastname = mg.StringField()

class OffersStat(mg.Document):
	performer_id_index = Index().ascending('performer_id').unique()
	performer_id_index.ascending('offer_id').unique()

	performer_id = mg.StringField()
	offer_id = mg.StringField()
	done = mg.BoolField(default=False)
	date = mg.DateTimeField(default=datetime.now())

class Gifts(mg.Document):
	title = mg.StringField()
	price = mg.IntField()
	body = mg.StringField()

import unittest
if __name__ == "__main__":
	class PerformerTest(unittest.TestCase):
		def test_user_id(self):
			user = Performer(user_id="qqqq",oauth_token="1223")
			user.save()
			q = Performer.query.filter(Performer.user_id =="qqqq").first()
			print type(q)
			print q


	unittest.main()
