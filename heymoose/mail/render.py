from flask import render_template

def mail_from_template(filename, **kwargs):
	template = render_template(filename, **kwargs)
	html, subject = [part.strip() for part in template.split('=====MAIL_SUBJECT_SPLIT=====')]
	return subject, html