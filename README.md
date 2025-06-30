# DoxGen

DoxGen - an application to fill out and print templated documents.

Template formats:
- HTML
- [RML](https://www.reportlab.com/docs/rml-for-idiots.pdf)
- PDF form
- Documents:
  + OpenDocument (.odx)
  + Office Open XML (.docx)

Output: HTML, PDF.

## Advantages:

- Simple templates rendering into output document like HTML templating
- High-quality final PDF for predictable printing result
- Extending user defined template set using simple plugins subsystem
- Support most popular document formats as templates

## Content

- doc/ - documentation:
  - [HowTo install](doc/INSTALL.md)
  - [HowTo plugins](doc/Plugins.md)
  - [Apache web-server config sample](doc/doxgen.conf)
  - [Overwriting default settings sample](doc/local_setting.py)
- doxgen/ - project itself:
  - locale/ - Django std (i18n)
  - static/ - Django std
  - templates/ - Django std
  - misc/ - common useful things (utilities, templatetags etc)
  - core/ - plugins management and converters
  - plugins/ - user defined plugins
  - udf/ - common user defined functions for all of plugins
  - *.py - Django std

## Contrib

### Bundled artifacts:

- [django-templates-macros](https://github.com/twidi/django-templates-macros)
- [jquery](https://jquery.com/)
- [jquery.populate](https://github.com/dtuite/jquery.populate)
- [jquery.formset](https://gist.github.com/vandorjw/f884f0d51db3e7caaecd)
- [bytesize](https://github.com/danklammer/bytesize-icons) icons

## Requirements:

- python3-django (repo)
- python3-weasyprint (repo)
- *python3-pdfkit* (repo)
- trml2pdf
- python3-z3c.rml (custom):
  + [rlPyCairo](https://pypi.org/project/rlPyCairo/) (custom)
  + [svglib](https://github.com/deeplook/svglib) (custom)

### Engines:
- HTML:
  + weasyprint
  + pdfkit (| wkhtmltopdf binary)
- RML:
  + trml2pdf
  + zope-z3c.rml
- PDF forms:
  + [PyPDFForm](https://github.com/chinapandaman/PyPDFForm) (reportlab, pypdf)
- ODF:
  + libreoffice
  + pandoc
