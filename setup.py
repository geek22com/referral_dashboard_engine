import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_package_data(root_dir, exts):
	data = []
	for root, _dirnames, filenames in os.walk(root_dir):
		for filename in filenames:
			if filename.lower().endswith(exts):
				data.append(os.path.join(root[len(root_dir)+1:], filename))
	return {'' : data}

setup(
	name = "frontend",
	version = "1.0",
	author = "HeyMoose",
	author_email = "heymoose@heymoose.com",
	description = ("Heymoose frontened "
	                               "Using heymoose backend flask mongodb uwsgi"),
	license = "Commercial",
	keywords = "commercial",
	url = "https://github.com/kshilov/frontend",
	packages=find_packages(),
	include_package_data = True,
	package_data = find_package_data('./heymoose', ('.html', '.css', '.js', '.png', '.gif', '.jpg')),
	install_requires = ['flask>=0.7', 'wtforms', 'flask-mongoalchemy', 'uwsgi', 
						'lxml', 'restkit', 'amqplib', 'python-dateutil==1.5', 'PIL'],
	long_description=read('README'),
)

