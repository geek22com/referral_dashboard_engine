#@PydevCodeAnalysisIgnore
from werkzeug import check_password_hash, generate_password_hash 
from Crypto.Cipher import AES 
import random, string, base64, time, uuid, os

def generate_uid(size, chars=string.ascii_letters+string.digits):
	return ''.join(random.choice(chars) for _x in range(size))

def generate_unique_filename():
	return '{0}{1}{2}'.format(int(time.time() * 100000), str(uuid.uuid4())[:8], os.getpid())

def aes_encrypt(key, data):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.encrypt(str(data))

def aes_decrypt(key, data):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.decrypt(data)


def aes_base64_encrypt(key, data, urlsafe=False):
	bytes = aes_encrypt(key, data)
	return base64.urlsafe_b64encode(bytes) if urlsafe else base64.b64encode(bytes)

def aes_base64_decrypt(key, data, urlsafe=False):
	bytes = base64.urlsafe_b64decode(str(data)) if urlsafe else base64.b64decode(str(data))
	return aes_decrypt(key, bytes)
	
	
def aes_base16_encrypt(key, data):
	bytes = aes_encrypt(key, data)
	return base64.b16encode(bytes)

def aes_base16_decrypt(key, data, casefold=True):
	bytes = base64.b16decode(str(data), casefold)
	return aes_decrypt(key, bytes)