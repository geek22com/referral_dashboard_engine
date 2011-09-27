all:
	rm -rf ./frontend_deb
	mkdir ./frontend_deb
	cp -rf ./heymoose ./frontend_deb/
	cp README ./frontend_deb/
	cp ./frontend_nginx.conf ./frontend_deb/
	cp ./heymoose_production.py ./frontend_deb/
	cp ./setup.py ./frontend_deb/
	cp ./uwsgi ./frontend_deb/
	tar czf frontend_deb.tar.gz ./frontend_deb
	rm -rf ./frontend_deb

clean:
	rm -rf frontend_deb*
	rm -rf $(CURDIR)/debian/frontend
