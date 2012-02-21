from heymoose import app
from heymoose.mail import smtp, render

from_address = app.config.get('MAIL_FROM_ADDRESS')
admins = app.config.get('MAIL_ADMINS')
	
def admin_list_add_failed(user):
	subject, text, html = render.mail_from_template('mail/admin-list-add-failed.html', user=user)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_feedback_added(contact):
	subject, text, html = render.mail_from_template('mail/admin-feedback-added.html', contact=contact)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_user_blocked(user, admin, reason):
	subject, text, html = render.mail_from_template('mail/admin-user-blocked.html', user=user, admin=admin, reason=reason)
	smtp.send_multipart(from_address, admins, subject, text, html)

def admin_order_created(user, order):
	subject, text, html = render.mail_from_template('mail/admin-order-created.html', user=user, order=order)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_order_changed(user, order):
	subject, text, html = render.mail_from_template('mail/admin-order-changed.html', user=user, order=order)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_order_blocked(order, admin, reason):
	subject, text, html = render.mail_from_template('mail/admin-order-blocked.html', order=order, admin=admin, reason=reason)
	smtp.send_multipart(from_address, admins, subject, text, html)

def admin_order_unblocked(order, admin):
	subject, text, html = render.mail_from_template('mail/admin-order-unblocked.html', order=order, admin=admin)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
def admin_order_moderation_failed(order, admin, reason):
	subject, text, html = render.mail_from_template('mail/admin-order-moderation-failed.html', order=order, admin=admin, reason=reason)
	smtp.send_multipart(from_address, admins, subject, text, html)
	
	
def user_confirm_email(user):
	subject, text, html = render.mail_from_template('mail/user-confirm-email.html', user=user)
	smtp.send_multipart(from_address, [user.email], subject, text, html)
	
def user_blocked(user, reason):
	subject, text, html = render.mail_from_template('mail/user-blocked.html', user=user, reason=reason)
	smtp.send_multipart(from_address, [user.email], subject, text, html)
	
def user_order_blocked(order, reason):
	subject, text, html = render.mail_from_template('mail/user-order-blocked.html', order=order, reason=reason)
	smtp.send_multipart(from_address, [order.user.email], subject, text, html)
	
def user_order_unblocked(order):
	subject, text, html = render.mail_from_template('mail/user-order-unblocked.html', order=order)
	smtp.send_multipart(from_address, [order.user.email], subject, text, html)
	
def user_order_moderation_failed(order, reason):
	subject, text, html = render.mail_from_template('mail/user-order-moderation-failed.html', order=order, reason=reason)
	smtp.send_multipart(from_address, [order.user.email], subject, text, html)

def user_order_priced_off(orders, c):
	emails = list(set([order.user.email for order in orders]))
	subject, text, html = render.mail_from_template('mail/user-order-priced-off.html', c=c)
	smtp.send_multipart_bulk(from_address, emails, subject, text, html)