import sys
sys.path.append("/home/kshilov/Prg/tuta/apache_configuration/frontend")
from heymoose.db.connection import connection
import random

def next_qa():
	first = random.randint(10000, 100000)
	second = random.randint(1, 10)
	return (first, second)

for i in range(1000):
	first, second = next_qa()
	question = str(first) + " + " + str(second) + " =?"
	answer = str(first + second) 
	args = {'question': question,
			'answer': answer}
	query = "INSERT INTO captcha (question, answer) VALUES(%(question)s, %(answer)s)"
	connection.execute_query(query, args)

