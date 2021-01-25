# DoxGen

Document generator

### Formats:

- Input: HTML, RML, PDF form, FODx
- Output: pdf, html, ~~svg~~, png (reportlab.graphics.RenderPM)

## Features:
- Anon:
  - *watermarks*
  - *submit delay*
  - *email dl PDF URL*
  - html preview
- Registered:
  - html download
  - pdf preview
  - pdf download
- X:
  - impex data
  - email pdfs
  - store data [in cookies/browser storge]

### Content
- doc/ - documentation
  - [ChangeLog](doc/ChangeLog.md)
  - [Installation](doc/INSTALL.md)
  - [ToDo list](doc/TODO.md)
- src/ - project itself
  - locale/ - Django std (i18n)
  - static/ - Django std
  - templates/ - Django std
  - misc/ - common usual things (utilities, templatetags etc)
  - core/ - plugins management and converters
  - plugins/ - user defined plugins
  - udf/ - user defined functions, commons for all of plugins
  - *.py - Django std

### Samples
- 0: html (Пример)
- 1: html (Заявление)
- ~~2~~: xhtml (Форма 21001) - use SSRF (84)
- 3: html (Форма ПД-4сб)
- 4: html (Доверенность форма м2)
- 5: rml/xpdf (Уведомление мигранта) - use SSRF (84)
- ~~6~~: xhtml (Реквизиты фирмы) - use Okved (1845)
- 7: xpdf (Форма 26.2-1)

## Contrib:
- [django-templates-macros](https://github.com/twidi/django-templates-macros)
- [jquery](https://jquery.com/)
- [jquery.populate](https://github.com/dtuite/jquery.populate) - to fill forms w/ sample
- jquery.formset - for dynamic form rows add ([src1](https://github.com/nortigo/jquery-formset) or [src2](https://github.com/elo80ka/django-dynamic-formset)
- icons: [bytesize](https://github.com/danklammer/bytesize-icons)
