# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import developer_only
from heymoose.views.work import *
import heymoose.core.actions.apps as apps

def app_form_template(form_params=None):
	app_form = forms.AppForm()
	if form_params:
		app_form.appcallback.data = form_params['appcallback']

	g.params['appform'] = app_form
	return render_template('app-creation-form.html', params = g.params)


@frontend.route('/app_form', methods=['GET'])
@developer_only
def app_form():
	return app_form_template()


@frontend.route('/create_app', methods=['POST'])
@developer_only
def create_app():
	#TODO проверка данных
	app_form = forms.AppForm(request.form)
	if request.method == "POST" and app_form.validate():
		apps.add_app(user_id=g.user.id,
						callback=app_form.appcallback.data)
		return redirect(url_for('user_cabinet', username=g.user.nickname))

	flash_form_errors(app_form.errors.values(), 'apperror')
	return app_form_template(request.form)

@frontend.route('/delete_app/<app_id>', methods=['POST', 'GET'])
@developer_only
def delete_app(app_id):
	print "Going to delete app"
	apps.delete_app(app_id)
	return redirect(url_for('user_cabinet', username=g.user.nickname))