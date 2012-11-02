from heymoose import app
from heymoose.mail import render

admins = app.config.get('MAIL_ADMINS')


# Admin emails

def admin_list_add_failed(user):
	subject, html = render.mail_from_template('mail/admin-list-add-failed.html', user=user)
	app.mail.send_message(subject=subject, html=html, recipients=admins)


def admin_feedback_added(contact):
	subject, html = render.mail_from_template('mail/admin-feedback-added.html', contact=contact)
	app.mail.send_message(subject=subject, html=html, recipients=admins)

	
def admin_user_blocked(user, admin, reason):
	subject, html = render.mail_from_template('mail/admin-user-blocked.html', user=user, admin=admin, reason=reason)
	app.mail.send_message(subject=subject, html=html, recipients=admins)


# User emails
	
def user_confirm_email(user):
	subject, html = render.mail_from_template('mail/user-confirm-email.html', user=user)
	app.mail.send_message(subject=subject, html=html, recipients=[user.email])


def user_restore_password(user, password):
	subject, html = render.mail_from_template('mail/user-restore-password.html', user=user, password=password)
	app.mail.send_message(subject=subject, html=html, recipients=[user.email])

	
def user_blocked(user, reason):
	subject, html = render.mail_from_template('mail/user-blocked.html', user=user, reason=reason)
	app.mail.send_message(subject=subject, html=html, recipients=[user.email])


def user_grant_approved(offer, affiliate):
	subject, html = render.mail_from_template('mail/user-grant-approved.html', offer=offer)
	app.mail.send_message(subject=subject, html=html, recipients=[affiliate.email])


def user_grant_rejected(offer, affiliate, reason):
	subject, html = render.mail_from_template('mail/user-grant-rejected.html', offer=offer, reason=reason)
	app.mail.send_message(subject=subject, html=html, recipients=[affiliate.email])


def user_grant_blocked(offer, affiliate, reason):
	subject, html = render.mail_from_template('mail/user-grant-blocked.html', offer=offer, reason=reason)
	app.mail.send_message(subject=subject, html=html, recipients=[affiliate.email])

