import random
from heymoose.db.models import Captcha
def check_captcha(c_id, answer):
	if not c_id or not answer:
		return None
	captcha = Captcha.query.filter(Captcha.c_id == int(c_id)).first()
	if captcha:
		if captcha.answer != answer:
			return None
		
		return captcha
	else:
		return None

def get_random(min=1, max=1000):
	c_id = random.randint(min, max)
	return Captcha.query.filter(Captcha.c_id == int(c_id)).first()
