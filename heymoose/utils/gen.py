from werkzeug import check_password_hash, generate_password_hash
import random, string

def generate_uid(size, chars=string.ascii_letters+string.digits):
	return ''.join(random.choice(chars) for _x in range(size))

