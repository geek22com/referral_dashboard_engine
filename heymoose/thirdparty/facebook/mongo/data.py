from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.fields import NumberField
from heymoose import mg
from mongoalchemy.document import Index

class Performer(mg.Document):
	user_id_index = Index().ascending('user_id').unique()
	
	user_id = mg.StringField()
	name = mg.StringField()
	oauth_token = mg.StringField()
	expires = mg.IntField()
	dirty = mg.BoolField(default=False)
	fullname = mg.StringField()
	firstname = mg.StringField()
	lastname = mg.StringField()

class Donations(mg.Document):
	from_id = mg.StringField()
	to_id = mg.StringField()
	gift_id = mg.StringField()

import unittest
if __name__ == "__main__":
	class PerformerTest(unittest.TestCase):
		def test_user_id(self):
			user = Performer(name="qqqq")
			user.save()
			q = Performer.query.filter(Performer.user_id == long(1233))
			print type(q)
			print q


	unittest.main()
