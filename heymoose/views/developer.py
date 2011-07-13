# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import Developer

@frontend.route('/become_developer')
@auth_only
def become_developer():
	developer_profile = Developer.get_developer(g.user.userid)
	if not developer_profile:
		developer_profile = Developer(g.user.userid)
		developer_profile.save()

	return redirect(url_for('user_cabinet', username=g.user.username))

@frontend.route('/register_developer/<username>',  methods=['POST'])
@auth_only
def register_developer(username):
	cursror = db_cursror.HDeveloperCursor(g.conn)
	developer_profile = cursror.get_developer(g.user['id'])
	if not developer_profile:
		new_developer(g.user['id'])
	return redirect(url_for('developer_page', username=g.user['name']))

@frontend.route('/developer/<username>')
@auth_only
def developer_page(username):

	cursror = db_cursror.HDeveloperCursor(g.conn)
	developer_profile = cursor.get_developer(g.user['id'])
	if developer_profile:
		developer_profile['already_developer'] = True
	return render_template('developer.html', args=developer_profile)

