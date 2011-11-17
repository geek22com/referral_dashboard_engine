# -*- coding: utf-8 -*-

from heymoose.utils.workers import app_logger, app_error
from restkit import request
from restkit import Resource
from restkit import forms
from functools import  partial
from restkit.errors import RequestFailed, RequestError
from heymoose import config
import sys
from lxml import etree

TIMEOUT = 1

URL_BASE = config.get('RESTAPI_SERVER')
TEST_PORT = 9345

def create_resource(base=URL_BASE):
	return Resource(base,
	                timeout=TIMEOUT)

def exec_request(http_call):
	try:
		return http_call()
	except (RequestFailed, RequestError) as inst:
		# We need to know url for debug info, but the system has broken, so raise it to the higher level
		if getattr(inst, 'response', False):
			app_logger.error(inst.response.final_url, exc_info=True)
		raise 

def get(path, base=URL_BASE, params_dict={}, renderer=etree.fromstring):
	app_logger.debug("get: base={0} path={1} params_dict={2}".format(base, path, str(params_dict)))
	resource = create_resource(base)
	response = exec_request(partial(resource.get,
	                            path=path,
	                            params_dict=params_dict))

	resp = response.body_string()
	if response.charset != 'utf8':
		resp = resp.decode('utf8')
	return renderer(resp)


def post(path, base=URL_BASE, params_dict={}):
	app_logger.debug("post: base={0} path={1} payload={2}".format(base, path, forms.form_encode(params_dict)))
	resource = create_resource()
	response = exec_request(partial(resource.post, path=path, payload=forms.form_encode(params_dict)))
	resp = response.body_string()
	if response.charset != 'utf8':
		resp = resp.decode('utf8')
	return resp

def put(path, base=URL_BASE, params_dict={}):
	app_logger.debug("put: base={0} path={1} payload={2}".format(base, path, forms.form_encode(params_dict)))
	resource = create_resource()
	exec_request(partial(resource.put,
	                              path=path,
	                              payload=forms.form_encode(params_dict)))

def delete(path, base=URL_BASE):
	app_logger.debug("delete: base={0} path={1}".format(base, path))
	resource = create_resource()
	exec_request(partial(resource.delete,
	                              path=path))

	### TESTS START HERE ###
import unittest
from flask import Flask
import sys
from os import fork, kill
import signal
from time import sleep

class RestTest(unittest.TestCase, object):
	def test_get(self):
		self.assertEqual(type( get(path="/") ), etree._Element)

	def test_post(self):
		post(path="/")

	def test_put(self):
		put(path="/")

	def test_delete(self):
		delete(path="/")

app = Flask(__name__)

@app.route("/", methods=['GET'])
def test_get_call():
	return "<a><b>Привет</b></a>"

@app.route("/", methods=['POST'])
def test_post_call():
	return  ""

@app.route("/", methods=['PUT'])
def test_put_call():
	return  ""

@app.route("/", methods=['DELETE'])
def test_delete_call():
	return  ""

### DEBUG FLASK APP SERVER ROUTINES ###
child_pid = 0
def start_server():
	print "START SERVER"
	pid = fork()
	if pid == 0:
		print "Child process"
		app.run(port=TEST_PORT)
		print "App died"
	else:
		sleep(2)
		return pid

def stop_server():
	if child_pid:
		print "Going to kill pid=%d" % child_pid
		kill(child_pid, signal.SIGTERM)

#TODO: write correct killer of app under debug :)
if __name__ == '__main__':
	try:
		URL_BASE = "http://127.0.0.1:%d%s" % (TEST_PORT, '/')
		child_pid = start_server()
		unittest.main()
	finally:
		stop_server()
		pass

