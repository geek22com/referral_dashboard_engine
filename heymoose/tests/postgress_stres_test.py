# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.db.models import Category
from heymoose.db.models import Blog
from heymoose.db.models import User
from heymoose.db.models import FeedBack
import random
import string
import sys
from datetime import datetime

def gen_random_mail(ln=10):
	return ''.join(random.choice(string.letters) for i in xrange(ln)) + "@" + ''.join(random.choice(string.letters) for i in xrange(ln)) + ".ru"

def gen_random_username(ln=20):
	return ''.join(random.choice(string.letters) for i in xrange(ln))

def str_diff_datetime(before, after):
	diff = after - before
	return " at seconds:" + str(diff.seconds) + "  microseconds:" + str(diff.microseconds)

@frontend.route('/test_register', methods=['GET', 'POST'])
def test_register():
		random.seed()
		try:
			username = gen_random_username()
			email = gen_random_mail()
			user = User(username=username,
						email=email,
						passwordhash=generate_password_hash("test_register"))
			before = datetime.now()
			user.save()
			after = datetime.now()
		except:
			return str(sys.exc_info())
		s_mess = "test_register Success " + str_diff_datetime(before=before, after=after)
		app_logger.debug(s_mess)
		return s_mess

@frontend.route('/test_show_category/<category_id>/<pagenum>')
def test_show_category(category_id=None, pagenum=None):
	if not category_id:
		return "test_show_category Fail"

	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	before = datetime.now()
	blogs = Blog.load_blogs_by_category(category_id=category_id, offset=offset)
	after = datetime.now()
	load_blogs_str = " load_blogs_by_category " + str_diff_datetime(before=before, after=after)

	if blogs:
		g.params['blogs'] = blogs

	before = datetime.now()
	categories = Category.load_categories()
	after = datetime.now()
	load_categories = " load_categories " + str_diff_datetime(before=before, after=after)
	if categories:
		g.params['categories'] = categories

	before = datetime.now()
	category = Category.load_category(category_id)
	after = datetime.now()
	load_category = " load_category " + str_diff_datetime(before=before, after=after)
	if category:
		g.params['category'] = category

	s_mess = "test_show_category Success " + \
		load_blogs_str + ":::" + \
		load_categories + ":::" + \
		load_category + "xxx"
	app_logger.debug(s_mess)
	return s_mess

@frontend.route('/test_login/<username>', methods=['GET', 'POST'])
def test_login(username):
	if username is None:
		return "test_login Fail"
	before = datetime.now()
	user = User.get_user(username)
	after = datetime.now()
	s_mess = "test_login Success " + str_diff_datetime(before=before, after=after)
	app_logger.debug(s_mess)
	return s_mess

@frontend.route('/test_feedback', methods=['GET', 'POST'])
def test_feedback():
	random.seed()
	try:
		email = gen_random_mail()
		comment = gen_random_username(256)
		feedback = FeedBack(email = email,
							comment = comment)
		before = datetime.now()
		feedback.save_new()
		after = datetime.now()
	except:
		return str(sys.exc_info())

	s_mess = "test_feedback Success " + str_diff_datetime(before=before, after=after)
	app_logger.debug(s_mess)
	return s_mess

