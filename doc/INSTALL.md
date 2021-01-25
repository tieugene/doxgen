# Install

## Converters:
- html:
  - &check; pdfkit (rpm, pip3)
    - wkhtmltopdf (CLI, w/ page break, rpm)
  - &check; weasyprint (py, rpm, pip3)
  - [*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf) (py, ~~rpm~~, pip3)
    - reportlab (rpm, pip3)
    - *PyPDF2* (rpm, pip3)
    - *html5lib* (rpm, pip3)
  - *iText.PdfWriter* via *.XMLWorker* (java)
- rml:
  - &check; trml2pdf (py, reportlab)
  - [*z3c.rml*](https://github.com/zopefoundation/z3c.rml)
- pdf form:
  - &check; jpype (py, rpm, pip3)
    - &check; iText (java)
  - *PyPDF2/4* (py, pure, rpm, w/ [issue](https://github.com/mstamy2/PyPDF2/issues/355))
- *doc[x]/fodt*:
  - ~~unoconv/python-webodt~~ libreoffice-headless

----
All:
* git ...
* wkhtmltopdf-static
* ln
* mkdir -p /mnt/shares/doxgen && chmod -R a+rwX /mnt/shares/doxgen
* ./manage.py syncdb
Production:
* httpd
* git ...
* chmod -R ...
* ./manage.py syncdb

```bash
sudo mkdir /usr/share/httpd/.config
sudo chmod a+rwX /usr/share/httpd/.config
sudo chown -R apache:apache /usr/share/httpd/.config
sudo chown :apache /usr/share/httpd
sudo chmod g+w /usr/share/httpd
sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
```

