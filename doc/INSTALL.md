# Install

## Converters:
- html:
  - &check; pdfkit (py, pip, rpm, ~~brew~~)
    - &rdsh; wkhtmltopdf (CLI, rpm, brew; , ?page break)
  - &check; weasyprint (py, pip, rpm, ~~brew~~)
  - [*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf) (py, pip, ~~rpm, brew~~)
    - reportlab (pip, rpm, ~~brew~~)
    - *PyPDF2* (pip, rpm)
    - *html5lib* (pip, rpm)
  - *iText.PdfWriter* via *.XMLWorker* (java)
- rml (&lArr; reportlab):
  - &check; trml2pdf (py, pip, *rpmable*)
  - [*z3c.rml*](https://github.com/zopefoundation/z3c.rml) (py, pip, *rpmable*)
- pdf form:
  - &check; jpype (py, pip, rpm)
    - &rdsh; &check; iTextPdf (java, ~~rpm~~, ~~brew~~)
  - *PyPDF2/4*? (py, pure, rpm, w/ [issue](https://github.com/mstamy2/PyPDF2/issues/355))
- *doc[x]/fodt*:
  - libreoffice-headless + python3-uno + [pyoo](https://github.com/mila/pyoo)

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

