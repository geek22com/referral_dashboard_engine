import sys
from heymoose import mg
from heymoose.db.models import Captcha
import random

def next_qa():
	first = random.randint(10000, 100000)
	second = random.randint(1, 10)
	return (first, second)

def generate_captcha(): 
	for i in range(1000):
		first, second = next_qa()
		question = str(first) + " + " + str(second) + " =?"
		answer = str(first + second) 
		args = {'question': question,
				'answer': answer}
		captcha = Captcha(c_id=i,answer=answer, question=question)
		captcha.save()
