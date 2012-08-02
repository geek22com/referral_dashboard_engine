from heymoose import app
from flaskext.script import Manager

manager = Manager(app)

import run, notify, createadmin