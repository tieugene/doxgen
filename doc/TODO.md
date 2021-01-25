# TODO

## 1. FixMe:
- i18n/l10n += form tip, about
- admin oops
- tpl multiline err:
  - 2 (Форма 21001)
  - 6 (Реквизиты фирмы)

## 2. ToDo:
- example: bill (multiline)
- watermark:
  - [html](https://codepen.io/YuvarajTana/pen/auiqx)
  - [pdf](https://stackabuse.com/working-with-pdfs-in-python-adding-images-and-watermarks/)
- xfdf (py)
- doc/
- std (requirements.txt, setup.py, coverage, *.spec)
  - Pycharm: Inspect code, Code cleanup, w3c validation
- remove django.* from core/convert:
  - httpresponse (<= convert returns header and payload)
  - template loader().render() => [jinga2 etc](https://wiki.python.org/moin/Templating)

## 3. Feature requests:
- select x2pdf engines in settings
- letsencrypt
- actions (- download filename = doxgen.ru.uuid.datetime.<ext>):
  - html2html in separate windows (target="_blank")
  - pdf-print
  - pdf-download
- buttons/icons as tags
- [flat icons](https://www.flaticon.com/) or [Awesome](https://fontawesome.com)
- html2pdf_itext
- doc_a: split into GET / POST
- modulelist as class
- tests (+tox.ini)
- move to flask (uvedomlenie), webpy (solo), web2py

## 4. Ideas:
- donate
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
- [PyPDF4](https://github.com/claird/PyPDF4)
- pdfminer.six - search [and *maybe* [replace](https://github.com/kanzure/pdfparanoia) PDF content
- trml2pdf.textBox == reportlab.platypus.Frame() + Paragraph()
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

## 6. Done:
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
+ PSS -> core/
+ plugins => plugin/ ([~~pre~~view.html] ~~list, read,  view~~):
  + zxxx.py
  + print.*
  + form.html
- 'dir'
- html preview for anon
- icons

### 7. Oops
- log to [RRDB](https://github.com/commx/python-rrdtool) - digits only

### 8. Icons

Action | Button.html | File.png | [Awesome](https://github.com/FortAwesome/Font-Awesome)
-------|-------------|----------|---------
favico | - |  favico | -
home | - | icon-home | +home
list | - | icon-list | +list
login | - | icon-enter | +sign-in-alt
logout | - | icon-exit | +sign-out-alt
admin | - | icon-settingsthree-gears | +tools<br/>+cog<br/>+cogs
info | - | icon-info-sign | +info
add row |  | *add* (16/32) | +plus-square
del row |  | *cross* (16/32) | +times<br/>+minus-square
*close* |  | *dialog-close* | +windows-close
clean | reset | edit-clear | +eraser
html-view | view | document-preview | +eye
*html-view-ext* |  | *text-html* | 
*html-dl* |  | *download* | 
pdf-view | print | AdobeReader9<br/>document-print-preview | +print
*pdf-view-ext* |  | *pdf-mime* | +file-pdf
pdf-dl |  | *pdf-adobe* | +download<br/>file-download<br/>file-download
*pdf-print* |  | *document-print* | 
pdf-email |  | *pdf-email* | +envelop
export | export | document-export | +file-export
import | import | document-import | +file-import
email-send |  | *dialog-ok* | +check-square
email-refuse |  | *dialog-cancel* | +times<br/>times-square<br/>+windows-close
