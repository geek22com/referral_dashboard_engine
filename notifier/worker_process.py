#!/usr/bin/python
"""
Test AMQP library.

Repeatedly receive messages from the demo_send.py
script, until it receives a message with 'quit' as the body.

2007-11-11 Barry Pederson <bp@barryp.org>

"""
from optparse import OptionParser
from time import sleep
import amqplib.client_0_8 as amqp
import os
import signal
import sys

EXCHANGE_NAME = "reports"
QUEUE_NAME = "reports.notify"
ROUTING_KEY = "notify"
children = []
child_channel = None
child_conn = None

def init(options):
	conn = amqp.Connection(options.host,
	                       userid=options.userid,
	                       password=options.password,
	                       ssl=options.ssl)
	
	ch = conn.channel()
	ch.exchange_declare(EXCHANGE_NAME,
						'direct',
						auto_delete=False)

	ch.queue_declare(queue=QUEUE_NAME)
	ch.queue_bind(queue=QUEUE_NAME,
					exchange=EXCHANGE_NAME,
					routing_key=ROUTING_KEY)


def callback(msg):
	for key, val in msg.properties.items():
		print ('%s: %s' % (key, str(val)))
	for key, val in msg.delivery_info.items():
		print ('> %s: %s' % (key, str(val)))

	print ('')
	print (msg.body)
	print ('-------')
	msg.channel.basic_ack(msg.delivery_tag)

def sigterm_handler(signum, frame):
	for pid in children:
		os.kill(pid, signal.SIGTERM)

def child_sigterm_handler(signum, frame):
	if child_channel:
		child_channel.close()
	if child_conn:
		child_conn.close()
	exit(0)

def child_routine(options):
	signal.signal(signal.SIGTERM, child_sigterm_handler)
	child_conn = amqp.Connection(options.host,
	                       userid=options.userid,
	                       password=options.password,
	                       ssl=options.ssl)

	child_channel = child_conn.channel()
	child_channel.access_request('/data', active=True, read=True)

	child_channel.basic_consume(QUEUE_NAME, callback=callback)

	while child_channel.callbacks:
		child_channel.wait()

	child_channel.close()
	child_conn.close()


def main():
	parser = OptionParser()
	parser.add_option('--host', dest='host',
						help='AMQP server to connect to (default: %default)',
						default='localhost')
	parser.add_option('-u', '--userid', dest='userid',
						help='userid to authenticate as (default: %default)',
						default='guest')
	parser.add_option('-p', '--password', dest='password',
						help='password to authenticate with (default: %default)',
						default='guest')
	parser.add_option('--ssl', dest='ssl', action='store_true',
						help='Enable SSL (default: not enabled)',
						default=False)
	parser.add_option('--worker_processes', dest='worker_processes',
						help='Enable SSL (default: not enabled)',
						default=1)
	options, args = parser.parse_args()
	print options.worker_processes
	if int(options.worker_processes) >= 20:
		print "to mush processes"
		exit(0)

	init(options)
	signal.signal(signal.SIGTERM, sigterm_handler)

	for i in range(int(options.worker_processes)):
		child = os.fork()
		if child: #parent
			children.append(child)
		else: #child
			child_routine(options)
			exit(0)

	for child in children:
		os.waitpid(child, 0)


import unittest
if __name__ == "__main__":
	main()
#	class QueueTest(unittest.TestCase):
#		def test_example(self):
#			pid = os.fork()
#			if pid == 0:
#				main()
#
#			pid1 = os.fork()
#			if pid1 == 0:
#				main()
#
#			sleep(5)
#
#			conn = amqp.Connection()
#			ch = conn.channel()
#			ch.access_request('/data', active=True, read=True)
#
#			for i in range(10):
#				msg = amqp.Message(u'Unicode hello' + unicode(i))
#				ch.basic_publish(msg,
#			                 exchange=EXCHANGE_NAME,
#			                 routing_key=ROUTING_KEY)
#
#			print "Send message"
#
#			while True:
#				pass
#
#	unittest.main()
