from flask import render_template

def mail_from_template(filename, **kwargs):
	template = render_template(filename, **kwargs)
	html, text, subject = [part.strip() for part in template.split('=====')]
	return subject, text, html