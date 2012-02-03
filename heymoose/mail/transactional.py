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