All:
	* django python-wkhtmltopdf
	* svn ...
	* wkhtmltopdf-static
	* ln
	* mkdir -p /mnt/shares/doxgen && chmod -R a+rwX /mnt/shares/doxgen
	* ./manage.py syncdb
Devel:
	*
Production:
	* httpd
	* svn ...
	* chmod -R ...
	* ./manage.py syncdb

Note: ln -s /usr/share/doxgen/static/admin /usr/lib/python2.7/site-packages/django/contrib/admin/static/admin

sudo mkdir /usr/share/httpd/.config
sudo chmod a+rwX /usr/share/httpd/.config
sudo chown -R apache:apache /usr/share/httpd/.config
sudo chown :apache /usr/share/httpd
sudo chmod g+w /usr/share/httpd
sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
