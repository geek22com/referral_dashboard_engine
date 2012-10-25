from heymoose import app, app_init_web
from heymoose.commands import manager

@manager.option('-t', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', default=8989)
def run(host, port):
	app_init_web(app)
	app.run(host=host, port=port)


