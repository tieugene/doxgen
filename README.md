# DoxGen

Document generator

## Requirements

- python3:
  - django 3.x (rpm)
  - trml2pdf
  - pdfkit (rpm)
  - ~~pymorphy2~~
- wkhtmltopdf (rpm)
- fonts:
  - [Liberation](https://github.com/liberationfonts/liberation-fonts) &copy; RH or [liberastica](https://code.google.com/archive/p/liberastika/) (cyr)
  - [Vera](https://download.gnome.org/sources/ttf-bitstream-vera/1.10/) &copy; Gnome
  - [Google's](https://github.com/google/fonts)
  - PT_ &copy; ParaType
  - [Microsoft core fonts](https://sourceforge.net/projects/corefonts/) &copy; Monotype (deb: ttf-mscorefonts-installer)

Uses:
- JS:
  - [jquery](https://jquery.com/download/) slim
  - [jquery.populate](https://github.com/dtuite/jquery.populate) to fill forms w/ sample
  - jquery.formset - for dynamic form rows add

## Formats:

- output: pdf, html, ~~svg~~
- input:
  - html:
    - &check;[*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf) (py, reportlab+PyPDF2+html5lib)
    - &check;[*weasyprint*](https://www.courtbouillon.org/weasyprint) (py, [pydyf](https://github.com/CourtBouillon/pydyf))
    - [pdfkit](https://github.com/JazzCore/python-pdfkit) | [*wkhtml2pdf*](https://github.com/wkhtmltopdf/wkhtmltopdf) (CLI, w/ [page break](https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2982))
  - rml:
    - &check;[*trml2pdf*](https://github.com/tieugene/trml2pdf) (py, reportlab)
  - pdf form:
    - [PyPDF2](https://github.com/mstamy2/PyPDF2) (py, pure, rpm) ([issue](https://github.com/mstamy2/PyPDF2/issues/355))
  - md: (?pagesize)
    - [pandoc](https://github.com/boisgera/pandoc) (via CLI)
    - py-md2pdf
    - py-markdown2pdf
    - ~~htmldoc~~?
  - rst:
     - [~~rst2pdf~~](https://github.com/ralsina/rst2pdf) (py|LaTeX)
  - rtf:
    - [ted](https://nllgg.nl/Ted/) (CLI, ~~rpm~~)
    - unrtf (>latex|rtf) (CLI)
  - doc[x]/odt:
    - unoconv/loffice service

## Samples
- 0: html (Пример)
- 1: html (Заявление)
- ~~2~~: xhtml (Форма 21001) - use SSRF (84)
- 3: html (Форма ПД-4сб)
- 4: html (Доверенность форма м2)
- ~~5~~ rml/xpdf (Уведомление мигранта) - use SSRF (84)
- ~~6~~: xhtml (Реквизиты фирмы) - use Okved (1845)
- 7: xpdf (Форма 26.2-1)

Required:
- html (|pdfkit(+wkhtmltopdf)/xhtml2pdf/weasy)
- rml (trml2pdf)
- xfdf (PyFPDF)

## Ideas
- use OrderedDict as model (or inmemory sqlite)
- html2rml
- smtp: chk domain and [user](https://github.com/un33k/python-emailahoy) exists:
  `socket.gethostbyname(domain:str)`
- rml2svg

## Try
- Google 'single application django project'
- PyPDF[2]
- python3-django-:
  - post_office
  - registration
  - rules
  - python3-mozilla-django-oidc : (OpenID)
  - [oauth-toolkit)(https://github.com/jazzband/django-oauth-toolkit)
- python3-flask-:
  - oauth : Adds OAuth support to Flask
  - oidc : An openID Connect support for Flask
  - openid : OpenID support for Flask
  - [authlib](https://github.com/lepture/flask-oauthlib)
- Google Page Speed

## TODO
+ python3
+ django 3.x:
  - i18n/l10n
  - syslog
- refucktor:
  - src &rArr; src/
  - mv manage.py doxgen_mgr
  - framework independent &rArr; subdir/ (modules, import &rarr; tpl &rarr; export):
    - consts.py
    - converter.py
    - dox_test_cs.py
    - dox/ref/
    - dox/tpl/ ?
  - std: setup.py, *.spec, tox.ini, doc/
- incapsulate plugins into a separate dir each
- move to flask (like uvedomlenie) or webpy (solo), web2py
- pymorphy2
- tpl/z*.py: bad import (Okved, SSRF; z0005_old)

## FIXME:
- process:
  + html2html
  + html2pdf (pdftk, slow)
  + rml2pdf
  - xfdf
- converter: ret header+content instead of response
- z0000: add a field or rm 'name'

# Trash

## Fixed:
+ tpl list is empty
+ uuid urls type
+ login/logout, admin
+ ~~/index forward to dox/~~ tpl_list url
+ object_list
+ doc_add
+ fill example (json sample empty)
+ pdf inplace (rm 'Content-disposition' from http response)
- / @ [admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-admin-templates):
  `cp django/contrib/admin/templates/base_site.html ./templates/admin/base_site.html | nano`

## Backends:
- HTML:
    - [~~htmldoc~~](https://github.com/michaelrsweet/htmldoc/) (CLI)
- RML:
    - [~~z3c.rml~~](https://github.com/tieugene/z3c.rml) (py, reportlab, zope.*) - devels unavailable
- XFDF:
  - [xfdftool](http://dik123.blogspot.com/2010/06/pdf.html)
  - ~~pdftk~~ (Java, can be server) - [RTFM](http://www.myown1.com/linux/pdf_formfill.shtml)
  - [~~pdfformfill~~](https://github.com/frainfreeze/pdformfill) (py, pdftk)
  - [~~pdfjinja~~](https://github.com/rammie/pdfjinja) (py, pdftk)
  - ~~xfdftool~~|java (CLI)
- XPS?
- misc:
  - [PyFPDF](https://github.com/reingart/pyfpdf) (py, pure) - create pdf (reportlab light)
  - [pdfminer.six](https://github.com/pdfminer/pdfminer.six) - extract fields


## OAuth providers
- google
- apple
- microsoft
- vk
- yandex
- twitter
- facebook
- github
- instagram
- [mail.ru](https://help.mail.ru/developers/oauth)
