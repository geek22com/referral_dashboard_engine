import sys, os
cmd_folder = os.path.dirname(os.path.abspath("/home/iceberg/heymoose/heymoose"))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
import __builtin__
__builtin__.DEBUG_CONFIG="/home/iceberg/heymoose/config_debug.py"
from heymoose import app as application
