# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms


@frontend.route('/vkontakte_app', methods=['GET', 'POST'])
def vkontakte_app():
	return render_template('heymoose-vkontakte.html')
