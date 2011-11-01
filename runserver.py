import sys, os

this_path = os.path.realpath(os.path.dirname(__file__))
project_path = os.path.join(this_path, "heymoose")
config_path = os.path.join(this_path, "config_debug.py")

if project_path not in sys.path:
	sys.path.insert(0, project_path)

import __builtin__
__builtin__.DEBUG_CONFIG = config_path

from heymoose import app
from heymoose.tests.gen_qa import generate_captcha

if __name__ == '__main__':
	generate_captcha()
	app.run(host="0.0.0.0", port=8989, debug=True)
