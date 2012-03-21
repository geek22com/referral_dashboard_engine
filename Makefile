
# Version of Python interpreter used in development
PYTHON_VERSION = 2.7.2

# Path to Python virtual environment
ENV_PATH = ~/.virtualenv/heymoose-frontend

# Path to Python interpreter in virtual environment
ENV_PY = $(ENV_PATH)/bin/python

# Path to pip requirements file
REQS_PATH = reqs.pip

# Path to Pythonbrew (https://github.com/utahta/pythonbrew)
PYTHONBREW_PATH = ~/.pythonbrew

# Path to Pythonbrew executable
PYTHONBREW = $(PYTHONBREW_PATH)/bin/pythonbrew


### TARGETS ###

# Installs deb packages required for development. 
dev-install-deps:
	echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" > \
		/etc/apt/sources.list.d/heymoose-frontend-dev.list
	apt-get update
	apt-get install build-essential libxml2 libxml2-dev libxslt1.1 libxslt1-dev \
		python-pip python-dev python-virtualenv mongodb-10gen curl

# Installs pythonbrew, creates virtual environment and installs all required
# python packages for development.
dev-deploy:
	curl -kL http://xrl.us/pythonbrewinstall | bash
	$(PYTHONBREW) install --no-test $(PYTHON_VERSION)
	$(PYTHONBREW) venv create --python=$(PYTHON_VERSION) --no-site-packages $(ENV_PATH)
	pip install -E $(ENV_PATH) -r $(REQS_PATH)

# Removes virtual environment.
dev-undeploy:
	rm -rf $(ENV_PATH)

# Runs development server using Python interpreter in virtual environment
dev-run:
	$(ENV_PY) runserver.py
	
dev-debug:
	$(ENV_PY) -m pdb runserver.py

dev-reset:
	sudo -u postgres psql -c "drop database heymoose;"
	sudo -u postgres psql -c "create database heymoose;"

dev-db:
	$(ENV_PY) dbfill.py
	
dev-py:
	$(ENV_PY) $(arg)

deb:
	debuild -uc -us -b
	debclean

all:
	$(ENV_PY) setup.py -q sdist

clean:
	rm -rf frontend_deb*
	rm -rf debian/frontend
	rm -rf dist
	rm -rf *.egg-info
