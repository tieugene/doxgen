# Install

Input:
  - html:
    - &check; pdfkit (rpm, pip3)
      - wkhtml2pdf (CLI, w/ page break, rpm)
    - &check; weasyprint (py, rpm, pip3)
    - *xhtml2pdf* (py, ~~rpm~~, pip3)
      - reportlab (rpm, pip3)
      - *PyPDF2* (rpm, pip3)
      - *html5lib* (rpm, pip3)
    - *iText.PdfWriter* via *.XMLWorker* (java)
  - rml:
    - &check; trml2pdf (py, reportlab)
  - pdf form:
    - &check; jpype (py, rpm, pip3)
      - &check; iText (java)
    - *PyPDF2* (py, pure, rpm, w/ [issue](https://github.com/mstamy2/PyPDF2/issues/355))
  - *doc[x]/odt*:
    - *unoconv/loffice service*

Uses:
- JS:
  - jquery (slim)
  - jquery.populate - to fill forms w/ sample
  - jquery.formset - for dynamic form rows add
- icons: [bytesize](https://github.com/danklammer/bytesize-icons)

## Converters:
  - html:
    - &check; pdfkit (rpm, pip3)
      - wkhtml2pdf (CLI, w/ page break, rpm)
    - &check; weasyprint (py, rpm, pip3)
    - *xhtml2pdf* (py, ~~rpm~~, pip3)
      - reportlab (rpm, pip3)
      - *PyPDF2* (rpm, pip3)
      - *html5lib* (rpm, pip3)
    - *iText.PdfWriter* via *.XMLWorker* (java)
  - rml:
    - &check; trml2pdf (py, reportlab)
  - pdf form:
    - &check; jpype (py, rpm, pip3)
      - &check; iText (java)
    - *PyPDF2* (py, pure, rpm, w/ [issue](https://github.com/mstamy2/PyPDF2/issues/355))
  - *doc[x]/odt*:
    - *unoconv/loffice service*

----
All:
	* git ...
	* wkhtmltopdf-static
	* ln
	* mkdir -p /mnt/shares/doxgen && chmod -R a+rwX /mnt/shares/doxgen
	* ./manage.py syncdb
Production:
	* httpd
	* svn ...
	* chmod -R ...
	* ./manage.py syncdb

```bash
Note: ln -s /usr/share/doxgen/static/admin /usr/lib/python2.7/site-packages/django/contrib/admin/static/admin

sudo mkdir /usr/share/httpd/.config
sudo chmod a+rwX /usr/share/httpd/.config
sudo chown -R apache:apache /usr/share/httpd/.config
sudo chown :apache /usr/share/httpd
sudo chmod g+w /usr/share/httpd
sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
```

