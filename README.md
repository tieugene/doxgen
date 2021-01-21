# DoxGen

Document generator

TODO: trml2pdf.textBox - use reportlab.platypus.Frame() + Paragraph()

## Requirements

- python3:
  - django 3.x (rpm):
    - [templates-macros](https://github.com/twidi/django-templates-macros)
  - trml2pdf
  - pdfkit (rpm)
  - jpype (rpm)
  - ~~pymorphy2~~
- wkhtmltopdf (CLI, rpm)
- iText-5.x.[itextpdf](https://github.com/itext/itextpdf/tree/develop/itext) (java)
  - jre
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
  - [jquery.formset](https://github.com/nortigo/jquery-formset) - for dynamic form rows add

## Formats:

- output: pdf, html, ~~svg~~, png (reportlab.graphics.RenderPM)
- input:
  - html:
    - &check;[pdfkit](https://github.com/JazzCore/python-pdfkit) | [*wkhtml2pdf*](https://github.com/wkhtmltopdf/wkhtmltopdf) (CLI, w/ [page break](https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2982))
    - [*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf) (py, reportlab+PyPDF2+html5lib)
    - [*weasyprint*](https://www.courtbouillon.org/weasyprint) (py, [pydyf](https://github.com/CourtBouillon/pydyf))
    - [*iText.PdfWriter*](https://ru.stackoverflow.com/questions/812556/itext-pdf-запись-html-в-pdf-в-кодировке-utf-8) via [XMLWorker](https://github.com/itext/itextpdf/blob/develop/xmlworker/src/main/java/com/itextpdf/tool/xml/XMLWorker.java)
  - rml:
    - &check;[trml2pdf](https://github.com/tieugene/trml2pdf) (py, reportlab)
  - pdf form:
    - &check;[iText](https://github.com/itext/itextpdf/tree/develop/itext/src/main/java/com/itextpdf/text/pdf) (java)
    - [*PyPDF2*](https://github.com/mstamy2/PyPDF2) (py, pure, rpm) ([issue](https://github.com/mstamy2/PyPDF2/issues/355))
  - doc[x]/odt:
    - unoconv/loffice service

## Samples
- 0: html (Пример)
- 1: html (Заявление)
- 2: xhtml (Форма 21001) - use SSRF (84)
- 3: html (Форма ПД-4сб)
- 4: html (Доверенность форма м2)
- 5: rml/xpdf (Уведомление мигранта) - use SSRF (84)
- 6: xhtml (Реквизиты фирмы) - use Okved (1845)
- 7: xpdf (Форма 26.2-1)

## Features:
- Anon:
  - *watermarks*
  - html preview
  - pdf download from trash
- Registered:
  - pdf preview
  - pdf download
- X:
  - multiprint
  - save/edit/del/copy
  - import/export data

----
## Ideas
- use OrderedDict as model (or inmemory sqlite)
- html2rml
- smtp: chk domain and [user](https://github.com/un33k/python-emailahoy) exists:
  `socket.gethostbyname(domain:str)`
- rml2svg

## Try
- Google 'single application django project'
- PyPDF[2]
- [iText7](https://github.com/itext/itext7) - Java (PDF Forms, HTML2PDF), ~~rpm~~
- Py &rArr; Java calls:
  - [JPype](https://github.com/jpype-project/jpype)  - Py&rArr;J call (rpm, pip3)
  - [Py4J](https://www.py4j.org) - Py&hArr;J call via 'server' (rpm, pypy)
  - [JCC](https://pypi.org/project/JCC/) - C++ Py&hArr;J glue code generator (~~rpm~~)
  - [jpy](https://github.com/bcdev/jpy) - Py&hArr;Java bridge (~~rpm~~)
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
- process:
  - html2pdf (py)
  - xfdf (py)

## FIXME:
- converter: ret header+content instead of response
- z0000: add a field or rm 'name'

----
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
+ / @ [admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-admin-templates):
  `cp django/contrib/admin/templates/base_site.html ./templates/admin/base_site.html | nano`
+ process:
  + html2html
  + html2pdf (pdftk, slow)
  + rml2pdf
  + xfdf (java)

## Backends:
- HTML:
  - [~~htmldoc~~](https://github.com/michaelrsweet/htmldoc/) (CLI)
- RML:
  - [~~z3c.rml~~](https://github.com/tieugene/z3c.rml) (py, reportlab, zope.*) - devels unavailable
- XFDF:
  - [~~pdftk~~](https://gitlab.com/pdftk-java/pdftk) (CLI, Java, ~~UTF8~~) - [RTFM](http://www.myown1.com/linux/pdf_formfill.shtml)
  - [~~pdfformfill~~](https://github.com/frainfreeze/pdformfill) (py, pdftk)
  - [~~pdfjinja~~](https://github.com/rammie/pdfjinja) (py, pdftk)
- md: (no sense; ?pagesize)
  - [pandoc](https://github.com/boisgera/pandoc) (via CLI)
  - py-md2pdf
  - py-markdown2pdf
  - ~~htmldoc~~?
- rst: (no sense)
  - [~~rst2pdf~~](https://github.com/ralsina/rst2pdf) (py|LaTeX)
- XPS?
- rtf:
  - [*ted*](https://nllgg.nl/Ted/) (CLI, ~~rpm~~)
  - *unrtf* (>latex|rtf) (CLI)
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
