# TODO

## 1. FixMe:
- std for deploy:
  - settings.py
  - local_settings.py
  - requirements.txt
  - .coveragerc
  - .gitattributes
  - .travis.yml
  + setup.py
  + MANIFEST.in
  + *.spec (TODO: += options)
- doc: Install

## 2. ToDo:
- watermark:
  - [html](https://codepen.io/YuvarajTana/pen/auiqx)
  - [pdf](https://stackabuse.com/working-with-pdfs-in-python-adding-images-and-watermarks/)
- xfdf (py)
- system fonts
- weasyprint vs pdfkit
- remove django.* from core/convert:
  - httpresponse (<= convert returns header and payload)
  - template loader().render() => [jinja2 etc](https://wiki.python.org/moin/Templating)
- Code cleanup:
  - Pycharm (Inspect code, Code cleanup, Coverage)
  - w3c validation
  - tests

## 3. Feature requests:
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
- tests (+tox.ini)
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
