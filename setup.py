from setuptools import setup, find_packages
import os, re

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Next two functions are nice shortcut for parsing pip requirements file
# instead of manually specifying dependencies in setup call below.
# Links:
#     http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy
#     https://github.com/cburgmer/pdfserver/blob/master/setup.py
def parse_requirements(file_name):
	requirements = []
	for line in open(file_name, 'r').read().split('\n'):
		if re.match(r'(\s*#)|(\s*$)', line):
			continue
		if re.match(r'\s*-e\s+', line):
			# TODO support version numbers
			requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
		elif re.match(r'\s*-f\s+', line):
			pass
		else:
			requirements.append(line)
	return requirements

def parse_dependency_links(file_name):
	dependency_links = []
	for line in open(file_name, 'r').read().split('\n'):
		if re.match(r'\s*-[ef]\s+', line):
			dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
	return dependency_links

# Finds package data with specified file extensions in root_dir and
# represents it in format for setup package_data parameter.
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
	description = ("Heymoose frontened. Using heymoose backend flask mongodb uwsgi"),
	license = "Commercial",
	keywords = "commercial",
	url = "https://github.com/kshilov/frontend",
	packages=find_packages(),
	include_package_data = True,
	package_data = find_package_data('./heymoose', tuple('.html .css .js .png .gif .jpg .ico'.split())),
	install_requires = parse_requirements('reqs.pip'),
	dependency_links = parse_dependency_links('reqs.pip'),
	long_description=read('README')
)

