# TODO

## 1. FixMe:
- convert: import on 1st import core.convert
- convert: fix xhtml2pdf cyr

## 2. ToDo:
- benchmark:
  - pdfkit vs weasyprint vs xhtml2pdf
  - trml2pdf vs z3c.rml
- converter expansion:
  - xfdf.py (pdf form) - PyPDF2/4, pikepdf, pdfminer.six
  - itext (html, pdf form)
  - ODF
- doxgen.spec: locale (rename, rm *.mo from src, mk *.mo on build)
- udf/ load list_* from csv
- doc: Plugins.md
- anti-robot:
  - all urls ar JS "void(){};"
  - JS-based in-place fields check (disable view/print buttons)
- watermark:
  - [html](https://codepen.io/YuvarajTana/pen/auiqx)
  - [pdf](https://stackabuse.com/working-with-pdfs-in-python-adding-images-and-watermarks/)
- wkhtmltopdf:
  - test pagebreak
  - test page number
  - what about wkhtmltopdf-static?
- Auth:
  - OAuth
  - register
- system fonts (? or use builtin AcroReader fonts only; see OpenERP)
- Code cleanup:
  - CSS: color,position,decoration,size
  - Pycharm (Inspect code, Code cleanup)
  - w3c validation
  - tests
    - &rdsh; .coveragerc
- misc github things (.travis.yml)
- sync with [Odoo](https://github.com/steedos/odoo7/tree/master/openerp/report/render)

## 3. Feature requests:
- XPS?
- set coverters in settings
- template loader().render() => [jinja2 etc](https://wiki.python.org/moin/Templating)
- lxml or sax
- select x2pdf engines in settings
- letsencrypt
- actions (- download filename = doxgen.ru.uuid.datetime.<ext>):
  - html-view-sep (target="_blank")
  - html-download
  - pdf-view-ext
  - pdf-download
  - pdf-print
- html2pdf_itext
- doc_a: split into GET / POST
- modulelist as class
- tests (+tox.ini), incl unittest, doctest; pytest?
- validate resulting html (tidylib, html5lib, [w3c](https://github.com/srackham/w3c-validator)
- move to lite frameworks (flask (uvedomlenie), webpy (solo), web2py)

## 4. Ideas:
- queues:
  - rendering [inmem, rrdb, ]
  - email
- use OrderedDict as model (or inmemory sqlite)
- disable cookie-based sessions
- smtp: chk domain and user (python-emailahoy) exists: `socket.gethostbyname(domain:str)`
- rml2svg
- rml2html
- html2rml
- [split settings](https://github.com/sobolevn/django-split-settings)
- pymorphy2

## 5. Try:
- [pikepdf](https://pypi.org/project/pikepdf/)
- [PyPDF4](https://github.com/claird/PyPDF4)
- pdfminer.six - search [and *maybe* [replace](https://github.com/kanzure/pdfparanoia)] PDF content
- trml2pdf.textBox == reportlab.platypus.Frame() + Paragraph()
- [RTFM](https://www.toptal.com/django/django-top-10-mistakes) Django good practice
- iText7 (Java, PDF Forms, HTML2PDF), ~~rpm~~
- Py &rArr; Java calls:
  - Py4J - Py&hArr;J call via 'server' (rpm, pypy)
  - JCC - C++ Py&hArr;J glue code generator (~~rpm~~)
  - jpy - Py&hArr;Java bridge (~~rpm~~)
- python3-django-:
  - python3-mozilla-django-oidc - OpenID ...
  - registration
  - post_office - async email
  - ~~rules~~ - per-object permissions
  - ~~oauth-toolkit~~ - OAuth provider
- python3-flask-:
  - oauth : Adds OAuth support to Flask
  - oidc : An openID Connect support for Flask
  - openid : OpenID support for Flask
  - authlib
- [Google Page Speed](https://developers.google.com/speed/pagespeed/insights/)

## 6. Plugins:
- HTML:
  - [*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf) (py, pip, ~~rpm, brew~~)
    - reportlab (pip, rpm, ~~brew~~)
    - *PyPDF2* (pip, rpm)
    - *html5lib* (pip, rpm)
  - *iText.PdfWriter* via *.XMLWorker* (java)
- RML:
  - [*z3c.rml*](https://github.com/zopefoundation/z3c.rml) (py, pip, *rpmable*)
- PDF form:
  - *PyPDF2/4*? (py, pure, rpm, w/ [issue](https://github.com/mstamy2/PyPDF2/issues/355))
- FODx:
  - libreoffice-headless + python3-uno + [pyoo](https://github.com/mila/pyoo)
