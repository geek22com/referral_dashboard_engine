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
