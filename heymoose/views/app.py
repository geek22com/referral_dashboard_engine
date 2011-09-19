# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import developer_only
from heymoose.views.work import *
import heymoose.core.actions.apps as apps

@frontend.route('/app_form', methods=['POST', 'GET'])
@developer_only
def app_form():
	apps.add_app(g.user.id)
	return redirect(url_for('user_cabinet', username=g.user.nickname))

