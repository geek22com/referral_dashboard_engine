# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import User 

@frontend.route('/become_developer')
@auth_only
def become_developer():
	if g.user and not g.user.is_developer():
		g.user.become_developer('FACEBOOK')

	return redirect(url_for('user_cabinet', username=g.user.username))
