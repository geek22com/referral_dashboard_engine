import random, string

def generate_uid(size, chars=string.ascii_letters+string.digits):
	return ''.join(random.choice(chars) for _x in range(size))

