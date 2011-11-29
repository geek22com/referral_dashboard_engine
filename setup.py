import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

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
    package_data = {'': ['templates/*.html', 
			'templates/facebook_app/*.html',
			'templates/gifts/*.html',
			'templates/admin/*.html'],
			'heymoose/admin' : ['static/js/*.js'],
			'heymoose' : ['static/js/*.js', 'static/css/*.css',
				'static/facebook_app/js/*.js', 'static/facebook_app/css/*.css',
				'static/vkontakte_app/js/.js', 'static/vkontakte_app/css/*.css']},
    install_requires = ['flask>=0.7', 'wtforms', 'flask-mongoalchemy', 'uwsgi', 'lxml', 'restkit', 'amqplib', 'python-dateutil==1.5'],
    long_description=read('README'),
)

