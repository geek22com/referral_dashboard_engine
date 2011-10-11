#!/usr/bin/python
"""
Test AMQP library.

Repeatedly receive messages from the demo_send.py
script, until it receives a message with 'quit' as the body.

2007-11-11 Barry Pederson <bp@barryp.org>

"""
from optparse import OptionParser
from time import sleep
import urllib2
import amqplib.client_0_8 as amqp
import syslog
import json
import os
import signal
import sys
from restkit import Resource
from restkit import forms
from functools import  partial
from restkit.errors import RequestFailed, RequestError


EXCHANGE_MLM_NAME = "reports"
EXCHANGE_ACTION_NAME = "events"
QUEUE_MLM_NAME = "reports.notify"
QUEUE_ACTION_NAME = "events.events"

ROUTING_KEY = "notify"
TIMEOUT = 20

def create_resource(base):
	return Resource(base,
	                timeout=TIMEOUT)

def exec_request(http_call):
	return http_call()

def post(path, base, params_dict={}):
	resource = create_resource(base)
	exec_request(partial(resource.post,
	                              path=path,
	                              payload=forms.form_encode(params_dict)))

def init(options):
	conn = amqp.Connection(options.host,
	                       userid=options.userid,
	                       password=options.password,
	                       ssl=options.ssl)
	
	ch = conn.channel()
	if options.hard_reset:
		syslog.syslog(syslog.LOG_INFO, "notifier hard_reset: remove all exchanges and queues from MQ")
		ch.exchange_delete(EXCHANGE_MLM_NAME)
		ch.exchange_delete(EXCHANGE_ACTION_NAME)
		ch.queue_delete(QUEUE_MLM_NAME)
		ch.queue_delete(QUEUE_ACTION_NAME)
		exit(0)

	#MLM
	ch.exchange_declare(EXCHANGE_MLM_NAME,
						'direct',
						auto_delete=False,
						durable=True)

	ch.queue_declare(queue=QUEUE_MLM_NAME)
	ch.queue_bind(queue=QUEUE_MLM_NAME,
					exchange=EXCHANGE_MLM_NAME,
					routing_key=ROUTING_KEY)

	#Action done
	ch.exchange_declare(EXCHANGE_ACTION_NAME,
						'fanout', # Fix after backend fix
						auto_delete=False,
						durable=True)

	ch.queue_declare(queue=QUEUE_ACTION_NAME)
	ch.queue_bind(queue=QUEUE_ACTION_NAME,
					exchange=EXCHANGE_ACTION_NAME)

def send_to_server(callback, params_dict):
	url_object = urllib2.urlparse.urlparse(callback)
	if url_object.port:
		base = "{0}://{1}:{2}".format(url_object.scheme, url_object.hostname, url_object.port)
	else:
		base = "{0}://{1}".format(url_object.scheme, url_object.hostname)
		
	post(url_object.path,
		base,
		params_dict=params_dict)


def action_done_callback(msg):
	if not msg.body:
		msg.channel.basic_ack(msg.delivery_tag)
		return
	message = json.loads(s=msg.body, encoding='utf8')
	try:
		send_to_server(message[u'callback'],
		               params_dict=dict(extId=message[u'extId'],
							offerId=message[u'offerId'],
							amount=message[u'amount']))

	except Exception as inst:
		syslog.syslog(syslog.LOG_ERR, "can't send message: {0}  msg_body: {1}  exception: {2}".format(message, msg.body, inst))

	msg.channel.basic_ack(msg.delivery_tag)

def mlm_callback(msg):
	if not msg.body:
		msg.channel.basic_ack(msg.delivery_tag)
		return

	message = json.loads(s=msg.body, encoding='utf8')
	try:
		send_to_server(message[u'callback'],
		               params_dict=dict(items=json.dumps(message[u'items']),
							appId=message[u'appId'],
							fromTime=message[u'fromTime'],
							toTime=message[u'toTime']))
	except Exception as inst:
		syslog.syslog(syslog.LOG_ERR, "can't send message: {0}  exception: {1}".format(message, inst))

	msg.channel.basic_ack(msg.delivery_tag)

def child_routine(options):
	syslog.syslog(syslog.LOG_INFO, "notifier started on host:{0} userid:{0}".format(options.host, options.userid))
	conn = amqp.Connection(options.host,
	                       userid=options.userid,
	                       password=options.password,
	                       ssl=options.ssl)

	ch = conn.channel()
	ch.access_request('/data', active=True, read=True)

	ch.basic_consume(QUEUE_MLM_NAME, callback=mlm_callback)
	ch.basic_consume(QUEUE_ACTION_NAME, callback=action_done_callback)

	if options.hand_send_action:
		syslog.syslog(syslog.LOG_INFO, "options.hand_send_action={0}".format(options.hand_send_action))
		action_message = amqp.Message(options.hand_send_action)
		action_done_callback(action_message)

	if options.hand_send_mlm:
		syslog.syslog(syslog.LOG_INFO, "options.hand_send_mlm={0}".format(options.hand_send_mlm))
		mlm_message = amqp.Message(options.hand_send_mlm)
		mlm_callback(mlm_message)

	while ch.callbacks:
		ch.wait()

	ch.close()
	conn.close()
	syslog.syslog(syslog.LOG_INFO, "notifier finished on host:{0} userid:{0}".format(options.host, options.userid))

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
	parser.add_option('--hard_reset', dest='hard_reset', action='store_true',
						help='Remove all exchanges and queues from MQ',
						default=False)

	parser.add_option('--hand_send_action', dest='hand_send_action',
						help='resend action message by hand',
						default=False)

	parser.add_option('--hand_send_mlm', dest='hand_send_mlm',
						help='resend mlm message by hand',
						default=False)


	options, args = parser.parse_args()
	try:
		init(options)
		child_routine(options)
	except Exception as inst:
		syslog.syslog(syslog.LOG_ERR, "exception: {0}".format(inst))
		syslog.syslog(syslog.LOG_ERR, "stacktrace: {0}".format(sys.exc_info()))

if __name__ == "__main__":
	main()

#	import unittest
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
#		def test_mlm_message(self):
#			body = """{"appId":1,"callback":"http://mlm.org/callback","fromTime":"2011-10-08T01:58:00.000+04:00","toTime":"2011-10-09T01:58:00.000+04:00","items":[{"extId":"ext2","passiveRevenue":"-0.90"},{"extId":"ext1","passiveRevenue":"0.90"}]}"""
#			body_action = """{"callback":"http://action.org/callback","extId":"ext1","offerId":"offer1","amount":"amount1"}"""
#			pid = os.fork()
#			if pid == 0:
#				main()
#
#			sleep(10)
#			conn = amqp.Connection()
#			ch = conn.channel()
#			ch.access_request('/data', active=True, read=True)
#
#			msg = amqp.Message(body)
#			ch.basic_publish(msg,
#		                 exchange=EXCHANGE_MLM_NAME,
#		                 routing_key=ROUTING_KEY)
#			sleep(5)
#			msg = amqp.Message(body_action)
#			ch.basic_publish(msg,
#		                 exchange=EXCHANGE_ACTION_NAME)
#
#			print "Send message"
#
#			while True:
#				pass
#
#		def test_action_message(self):
#			body = """{"callback":"http://action.org/callback","extId":"ext1","offerId":"offer1","amount":"amount1"]}"""
#			pid = os.fork()
#			if pid == 0:
#				main()
#
#			sleep(5)
#			conn = amqp.Connection()
#			ch = conn.channel()
#			ch.access_request('/data', active=True, read=True)
#
#			msg = amqp.Message(body)
#			ch.basic_publish(msg,
#		                 exchange=EXCHANGE_ACTION_NAME)
#			print "Send message"
#
#			while True:
#				pass
#
#	unittest.main()
