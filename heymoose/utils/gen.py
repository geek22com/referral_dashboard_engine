from werkzeug import check_password_hash, generate_password_hash
from Crypto.Cipher import AES 
import random, string, base64

def generate_uid(size, chars=string.ascii_letters+string.digits):
	return ''.join(random.choice(chars) for _x in range(size))


def aes_base64_encrypt(key, data):
	obj = AES.new(key, AES.MODE_ECB)
	bytes = obj.encrypt(str(data))
	#return base64.urlsafe_b64encode(bytes)
	return base64.b16encode(bytes).lower()

def aes_base64_decrypt(key, data):
	obj = AES.new(key, AES.MODE_ECB)
	#bytes = base64.urlsafe_b64decode(str(data))
	bytes = base64.b16decode(str(data), True)
	return obj.decrypt(bytes)