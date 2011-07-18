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

def gen_random_mail(ln=10):
	return ''.join(random.choice(string.letters) for i in xrange(ln)) + "@" + ''.join(random.choice(string.letters) for i in xrange(ln)) + ".ru"

def gen_random_username(ln=20):
	return ''.join(random.choice(string.letters) for i in xrange(ln))

@frontend.route('/test_register', methods=['GET', 'POST'])
def test_register():
		random.seed()
		try:
			username = gen_random_username()
			email = gen_random_mail()
			user = User(username=username,
						email=email,
						passwordhash=generate_password_hash("test_register"))
			user.save()
		except:
			return str(sys.exc_info())

		return "test_register Success"

@frontend.route('/test_show_category/<category_id>/<pagenum>')
def test_show_category(category_id=None, pagenum=None):
	if not category_id:
		return "test_show_category Fail"

	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	blogs = Blog.load_blogs_by_category(category_id=category_id, offset=offset)
	if blogs:
		g.params['blogs'] = blogs

	categories = Category.load_categories()
	if categories:
		g.params['categories'] = categories

	category = Category.load_category(category_id)
	if category:
		g.params['category'] = category

	return "test_show_category Success"

@frontend.route('/test_login/<username>', methods=['GET', 'POST'])
def test_login(username):
	if username is None:
		return "test_login Fail"

	user = User.get_user(username)
	return "test_login Success"

@frontend.route('/test_feedback', methods=['GET', 'POST'])
def test_feedback():
	random.seed()
	try:
		email = gen_random_mail()
		comment = gen_random_username(256)
		feedback = FeedBack(email = email,
							comment = comment)
		feedback.save_new()
		return "test_feedback Success"
	except:
		return str(sys.exc_info())



