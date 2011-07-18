from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from heymoose.utils.workers import app_logger

def auth_only(func):
	def _inner_(*args, **kwargs):
		if 'user_id' not in session:
			#app_logger.error('Not in session auth_only')
			return redirect(url_for('register'))
		return func(*args, **kwargs)
	_inner_.__name__ = func.__name__
	return _inner_

def admin_only(func):
	def _inner_(*args, **kwargs):
		if 'user_id' not in session:
			return redirect(url_for('register'))
		if g.user.username != 'admin':
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

