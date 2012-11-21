# -*- coding: utf-8 -*-
from flask import render_template
from heymoose import app, signals
from heymoose.mail.flaskext import Message


admins = app.config.get('MAIL_ADMINS')


# Some shortcuts for common operations

def message_from_template(template_filename, template_args, **message_args):
	template = render_template(template_filename, **template_args)
	html, subject = [part.strip() for part in template.split('=====MAIL_SUBJECT_SPLIT=====')]
	return Message(subject=subject, html=html, **message_args)

def send_from_template(sender, template_filename, template_args, **message_args):
	message = message_from_template(template_filename, template_args, **message_args)
	sender.send(message)

def message_to_recipient(message, recipient):
	message.recipients = [recipient]
	return message


# Signal handlers

@signals.contacts_list_add_failed.connect
def contacts_list_add_failed(app, **kwargs):
	send_from_template(app.mail, 'mail/admin-list-add-failed.html', kwargs, recipients=admins)


@signals.new_feedback.connect
def new_feedback(app, **kwargs):
	send_from_template(app.mail, 'mail/admin-feedback-added.html', kwargs, recipients=admins)


@signals.user_blocked.connect
def user_blocked(app, notify_user=False, **kwargs):
	with app.mail.connect() as connection:
		send_from_template(connection, 'mail/admin-user-blocked.html', kwargs, recipients=admins)
		if notify_user:
			send_from_template(connection, 'mail/user-blocked.html', kwargs, recipients=[kwargs['user'].email])


@signals.confirmation_email_requested.connect
def confirmation_email_requested(app, **kwargs):
	send_from_template(app.mail, 'mail/user-confirm-email.html', kwargs, recipients=[kwargs['user'].email])


@signals.password_restore_requested.connect
def password_restore_requested(app, **kwargs):
	send_from_template(app.mail, 'mail/user-restore-password.html', kwargs, recipients=[kwargs['user'].email])


@signals.offer_blocked.connect
def offer_blocked(app, affiliates=None, notify_affiliates=False, **kwargs):
	with app.mail.connect() as connection:
		send_from_template(connection, 'mail/admin-offer-blocked.html', kwargs, recipients=admins)
		if notify_affiliates:
			message = message_from_template('mail/user-offer-blocked.html', kwargs)
			for affiliate in affiliates: connection.send(message_to_recipient(message, affiliate.email))


@signals.offer_unblocked.connect
def offer_unblocked(app, affiliates=None, notify_affiliates=False, **kwargs):
	with app.mail.connect() as connection:
		send_from_template(connection, 'mail/admin-offer-unblocked.html', kwargs, recipients=admins)
		if notify_affiliates:
			message = message_from_template('mail/user-offer-unblocked.html', kwargs)
			for affiliate in affiliates: connection.send(message_to_recipient(message, affiliate.email))


@signals.grant_approved.connect
def grant_approved(app, notify=False, **kwargs):
	if notify:
		send_from_template(app.mail, 'mail/user-grant-approved.html', kwargs, recipients=[kwargs['grant'].affiliate.email])


@signals.grant_rejected.connect
def grant_rejected(app, notify=False, **kwargs):
	if notify:
		send_from_template(app.mail, 'mail/user-grant-rejected.html', kwargs, recipients=[kwargs['grant'].affiliate.email])


@signals.grant_blocked.connect
def grant_blocked(app, notify=False, **kwargs):
	if notify:
		send_from_template(app.mail, 'mail/user-grant-blocked.html', kwargs, recipients=[kwargs['grant'].affiliate.email])
