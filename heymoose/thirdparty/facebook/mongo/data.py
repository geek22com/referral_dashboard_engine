from flaskext.mongoalchemy import BaseQuery
from mongoalchemy.fields import NumberField
from heymoose import mg

class Performer(mg.Document):
	name = mg.StringField()
	oauth_token = mg.StringField()
	expires = mg.IntField()
	user_id = mg.StringField()
	dirty = mg.BoolField(default=False)
	fullname = mg.StringField()
	firstname = mg.StringField()
	lastname = mg.StringField()


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
