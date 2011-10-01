import sys, os
cmd_folder = os.path.dirname(os.path.abspath("/home/ksshilov/heymoose_debug/frontend/frontend-1.0/heymoose"))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
import __builtin__
__builtin__.DEBUG_CONFIG="/home/ksshilov/heymoose_debug/frontend/frontend-1.0/config_debug.py"
from heymoose import app as application
