from heymoose import app
from heymoose.mail import smtp, render

from_address = app.config.get('MAIL_FROM_ADDRESS')
admins = app.config.get('MAIL_ADMINS')

def admin_order_created(user, order):
	subject, text, html = render.mail_from_template('mail/admin-order-created.html', user=user, order=order)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_list_add_failed(user):
	subject, text, html = render.mail_from_template('mail/admin-list-add-failed.html', user=user)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_feedback_added(contact):
	subject, text, html = render.mail_from_template('mail/admin-feedback-added.html', contact=contact)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_user_blocked(user, admin, reason):
	subject, text, html = render.mail_from_template('mail/admin-user-blocked.html', user=user, admin=admin, reason=reason)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
	
def user_confirm_email(user):
	subject, text, html = render.mail_from_template('mail/user-confirm-email.html', user=user)
	smtp.send_multipart(from_address, [user.email], subject, text, html)
	
def user_blocked(user, reason):
	subject, text, html = render.mail_from_template('mail/user-blocked.html', user=user, reason=reason)
	print subject
	print text
	print html
	smtp.send_multipart(from_address, [user.email], subject, text, html)
	