# DoxGen

Document generator

TODO: trml2pdf.textBox - use reportlab.platypus.Frame() + Paragraph()

## 1. Requirements

- python3:
  - django 3.x (rpm, pip):
    - templates-macros
  - trml2pdf
  - html2pdf (one from):
    - pdfkit (rpm, pip)
    - weasyprint (rpm, pip)
  - jpype (rpm, pip)
- wkhtmltopdf (CLI, rpm)
- itextpdf (java, ~~rpm~~)
  - jre (rpm)
- fonts: Liberation, Vera, Google's, ParaType, Microsoft core fonts 

Uses:
- JS:
  - jquery (slim)
  - jquery.populate - to fill forms w/ sample
  - jquery.formset - for dynamic form rows add

### Formats:

Output: pdf, html, ~~svg~~, png (reportlab.graphics.RenderPM)
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

### Features:
- Anon:
  - *watermarks*
  - *submit delay*
  - html preview
  - pdf download from trash (or email only)
- Registered:
  - html download
  - pdf preview
  - pdf download
- X:
  - impex data
  - email pdfs
  - store data in cookies

### Samples
- 0: html (Пример)
- 1: html (Заявление)
- ~~2~~: xhtml (Форма 21001) - use SSRF (84)
- 3: html (Форма ПД-4сб)
- 4: html (Доверенность форма м2)
- 5: rml/xpdf (Уведомление мигранта) - use SSRF (84)
- ~~6~~: xhtml (Реквизиты фирмы) - use Okved (1845)
- 7: xpdf (Форма 26.2-1)

### Content
- doc/ - documentation
- src/ - project itself
  - templates/ - common html templates
  - static/
  - core/
  - plugin/z*/ - plugin (code, forms, templates)

----
## 2. Tasks
### FIXME:
- html preview for anon
- converter: ret header+content instead of response
- html2html in separate windows (standalone), download
- buttons (13): home[/list]/login/logout/admin/info/create/cancel/clean/html-view|dl/pdf-view|dl
- tpl/z000{2,6}.py: bad import (SSRF, Okved (2-lvl treeview)) -> list

### ToDo:
- letsencrypt
- watermark
- refucktoring:
  - framework independent &rArr; subdir/ ({consts,converter,dox_test_cs}.py,dox/ref/,dox/tpl/)
  - plugins => plugin/z###/* (dox/tpl/*.py, templates/{form/list/print/read/view}
  - std: requirements.txt, setup.py, *.spec, tox.ini, doc/
- move to flask (like uvedomlenie) or webpy (solo), web2py
- plugin scheme: json/xml+td
- xfdf (py)
- i18n/l10n
- tests

### Ideas:
- convert tpl[][][] into tpl.attr.attr...
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

### Try:
- [RTFM](https://www.toptal.com/django/django-top-10-mistakes) Django good practice
- plugun form/list/etc as <embed>
- Google 'single application django project'
- PyPDF2
- iText7- Java (PDF Forms, HTML2PDF), ~~rpm~~
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
- Google Page Speed

----
## 3. Trash

### Done:
+ python3
+ Django 3.x
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
+ refuctor:
  + src &rArr; src/
  + mv manage.py ~~doxgen_mgr~~ manage (sh)
+ html2pdf (py)
+ Log to Logging (+IP/agent[/POST_data])
+ app-less (mv drc/dox/ src.db/)

### Oops
- log to [RRDB](https://github.com/commx/python-rrdtool) - digits only

### Backends:
- HTML:
  - ~~htmldoc~~ (CLI)
- RML:
  - ~~z3c.rml~~ (py, reportlab, zope.*) - devels unavailable
- XFDF:
  - ~~pdftk~~ - (CLI, Java, ~~UTF8~~)
  - ~~pdfformfill~~ (py, pdftk)
  - ~~pdfjinja~~ (py, pdftk)
- md: (no sense; ?pagesize)
  - pandoc (via CLI)
  - *py-md2pdf*
  - *py-markdown2pdf*
  - ~~*htmldoc*~~?
- rst: (no sense)
- XPS?:
- rtf:
  - *ted* (CLI, ~~rpm~~)
  - *unrtf* (>latex|rtf) (CLI)
- misc:
  - PyFPDF (py, pure) - create pdf (reportlab light)
  - pdfminer.six - extract fields


### OAuth providers
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

====
## 4. Resources

### py:
- Django:
  - -[templates-macros](https://github.com/twidi/django-templates-macros)
  - -[oauth-toolkit](https://github.com/jazzband/django-oauth-toolkit)
  - [python3-mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc)
  - -[post_office](https://github.com/ui/django-post_office)
  - -[registration](https://github.com/ubernostrum/django-registration/)
  - -[rules](https://pypi.org/project/django-rules/)
- [trml2pdf](https://github.com/tieugene/trml2pdf)
- [pdfkit](https://github.com/JazzCore/python-pdfkit)
- [JPype](https://github.com/jpype-project/jpype) 
- [*xhtml2pdf*](https://github.com/xhtml2pdf/xhtml2pdf)
- [*weasyprint*](https://www.courtbouillon.org/weasyprint)
- [*pydyf*](https://github.com/CourtBouillon/pydyf)
- [*PyPDF2*](https://github.com/mstamy2/PyPDF2)
  - [issue](https://github.com/mstamy2/PyPDF2/issues/355)
- [PyFPDF](https://github.com/reingart/pyfpdf)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- [z3c.rml](https://github.com/tieugene/z3c.rml)
- [Py4J](https://www.py4j.org)
- [JCC](https://pypi.org/project/JCC/)
- [jpy](https://github.com/bcdev/jpy)
- [pdfformfill](https://github.com/frainfreeze/pdformfill)
- [pdfjinja](https://github.com/rammie/pdfjinja)
- [python-emailahoy](https://github.com/un33k/python-emailahoy)
### JS:
- [jquery](https://jquery.com/download/)
- [jquery.populate](https://github.com/dtuite/jquery.populate)
- [jquery.formset](https://github.com/nortigo/jquery-formset)
### Java
- iText.[itextpdf](https://github.com/itext/itextpdf/tree/develop/itext/src/main/java/com/itextpdf/text/pdf)
  - [*iText.PdfWriter*](https://ru.stackoverflow.com/questions/812556/itext-pdf-запись-html-в-pdf-в-кодировке-utf-8)
  - [XMLWorker](https://github.com/itext/itextpdf/blob/develop/xmlworker/src/main/java/com/itextpdf/tool/xml/XMLWorker.java)
- [iText7](https://github.com/itext/itext7) 
- [pdftk](https://gitlab.com/pdftk-java/pdftk)
  - [RTFM](http://www.myown1.com/linux/pdf_formfill.shtml)
### bin:
- [wkhtml2pdf](https://github.com/wkhtmltopdf/wkhtmltopdf)
  - [page break](https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2982)
- [Ted](https://nllgg.nl/Ted/) (CLI, ~~rpm~~)
- [htmldoc](https://github.com/michaelrsweet/htmldoc/)
- [pandoc](https://github.com/boisgera/pandoc)
### fonts:
- [Liberation](https://github.com/liberationfonts/liberation-fonts) &copy; RH or [liberastica](https://code.google.com/archive/p/liberastika/) (cyr)
- [Vera](https://download.gnome.org/sources/ttf-bitstream-vera/1.10/) &copy; Gnome
- [Google's](https://github.com/google/fonts)
- PT_ &copy; ParaType
- [Microsoft core fonts](https://sourceforge.net/projects/corefonts/) &copy; (deb: ttf-mscorefonts-installer)

> Every copy of Acrobat Reader comes with 14 standard fonts built in:<br/>
> Fixed: Courier[-Bold|-Oblique|-BoldOblique]<br/>
> Proportional: Helvetica[-Bold|-Oblique|-BoldOblique], Times-{Roman,Bold,Italic,BoldItalic}, Symbol, ZapfDingbats

