from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from heymoose.utils.workers import app_logger

#TODO create one decorator
#problem: don't know how to pass parameter to decorator(Flask specific)
# auth('devloper'), auth('customer') ....


def auth_only(func):
    def _inner_(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('register'))
        if not g.user.is_somebody():
	        return redirect(url_for('role_detect'))
        return func(*args, **kwargs)
    _inner_.__name__ = func.__name__
    return _inner_

def oauth_only(func):
	def _inner_(*args, **kwargs):
		if 'access_token' not in session:
			app_logger.debug("oauth_only error: no access_token")
			abort(404)
		if 'facebook_user_id' not in session:
			app_logger.debug("oauth_only error: no user_id")
			abort(404)
		g.access_token = session['access_token']
		g.facebook_user_id = session['facebook_user_id']
		return func(*args, **kwargs)
	_inner_.__name__ = func.__name__
	return _inner_


def role_not_detected_only(func):
    def _inner_(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('register'))
        return func(*args, **kwargs)
    _inner_.__name__ = func.__name__
    return _inner_


def customer_only(func):
    def _inner_(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('register'))
        if not g.user.is_customer():
            return redirect(url_for('role_detect'))
        return func(*args, **kwargs)
    _inner_.__name__ = func.__name__
    return _inner_

def developer_only(func):
    def _inner_(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('register'))
        if not g.user.is_developer():
            return redirect(url_for('role_detect'))
        return func(*args, **kwargs)
    _inner_.__name__ = func.__name__
    return _inner_

def admin_only(func):
    def _inner_(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('register'))
        if not g.user.is_admin():
            return redirect(url_for('register'))
        return func(*args, **kwargs)
    _inner_.__name__ = func.__name__
    return _inner_


def singleton(cls):
	instances = {}
	def getinstance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	getinstance.__name__ = cls.__name__
	return getinstance

