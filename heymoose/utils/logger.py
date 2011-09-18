from heymoose.utils.workers import app_logger
import sys

def log_exception(inst):
	app_logger.error(inst)
	app_logger.error(sys.exc_info())
