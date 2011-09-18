# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import developer_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.views.work import *

@frontend.route('/app_form', methods=['POST', 'GET'])
@developer_only
def app_form():
	g.user.create_app()
	return redirect(url_for('user_cabinet', username=g.user.nickname))

