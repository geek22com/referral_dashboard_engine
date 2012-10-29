from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from heymoose import app
import smtplib

enabled = app.config.get('MAIL_ENABLED')
smtp_debug = app.debug
smtp_host = app.config.get('MAIL_SMTP_HOST')
smtp_port = app.config.get('MAIL_SMTP_PORT')
smtp_timeout = app.config.get('MAIL_SMTP_TIMEOUT')
smtp_username = app.config.get('MAIL_SMTP_USERNAME')
smtp_password = app.config.get('MAIL_SMTP_PASSWORD')


def create_multipart(fm, to, subject, text, html):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = fm
	msg['To'] = ', '.join(to)
	
	part_text = MIMEText(text, 'plain', 'utf-8')
	part_html = MIMEText(html, 'html', 'utf-8')
	msg.attach(part_text)
	msg.attach(part_html)
	return msg


def safe_connect():
	try:
		s = smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout)
		s.set_debuglevel(smtp_debug)
		s.login(smtp_username, smtp_password)
		return s
	except:
		app.logger.error(u'Failed to connect to SMTP server {0}:{1}'.format(smtp_host, smtp_port), exc_info=True)
		return None
	
def safe_disconnect(s):
	try:
		s.quit()
	except:
		app.logger.error(u'Failed do QUIT from SMTP server {0}:{1}'.format(smtp_host, smtp_port), exc_info=True)
	

def send_multipart(fm, to, subject, text, html):
	app.logger.info(u'Sending email with subject <{0}> to {1}'.format(subject, unicode(to)))
	if not enabled:
		app.logger.info(u'But emailing is disabled!')
		return
	s = safe_connect()
	if s is None: return
	try:
		msg = create_multipart(fm, to, subject, text, html)
		s.sendmail(fm, to, msg.as_string())
	except:
		app.logger.error(u'Failed to send mail with subject <{0}> to {1}'.format(subject, unicode(to)), exc_info=True)
	safe_disconnect(s)

def send_multipart_bulk(fm, to, subject, text, html):
	app.logger.info(u'Sending bulk email with subject <{0}> to {1}'.format(subject, unicode(to)))
	if not enabled:
		app.logger.info(u'But emailing is disabled!')
		return
	s = safe_connect()
	if s is None: return
	for rcpt in to:
		try:
			msg = create_multipart(fm, [rcpt], subject, text, html)
			s.sendmail(fm, [rcpt], msg.as_string())
		except:
			app.logger.error(u'Failed to send mail with subject <{0}> to {1}'.format(subject, unicode(to)), exc_info=True)
	safe_disconnect(s)



