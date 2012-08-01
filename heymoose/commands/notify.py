from heymoose import app, app_init_basic
from heymoose.commands import manager

@manager.command
def notify():
	app_init_basic(app)
	print 'OK'