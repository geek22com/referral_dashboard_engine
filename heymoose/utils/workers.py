from heymoose import app
from functools import partial

app_logger = app.logger
app_debug = partial(app.logger.debug, msg='', exc_info=True)
app_error = partial(app.logger.error, msg='', exc_info=True)
config = app.config
heymoose_app = app
