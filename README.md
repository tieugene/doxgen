# DoxGen

DoxGen - an application to fill out and print templated documents.

Input template formats:
- HTML (.html)
- [RML](https://www.reportlab.com/docs/rml-for-idiots.pdf) (.rml)
- PDF form (.pdf)
- OpenDocument Text (.odt)

Output: PDF

## Advantages:

- Simple templates rendering into output document like HTML templating
- High-quality final PDF for predictable printing result
- Extending user defined template set using simple plugins subsystem
- Support most popular document formats as templates

## Requirements:

- Django
- weasyprint (HTML engine)
- python3-pdfkit (HTML engine)
- trml2pdf (RML engine)
- z3c.rml2pdf (RML engine)
- [PyPDFForm](https://github.com/chinapandaman/PyPDFForm) (PDF form engine)
- libreoffice-writer (ODT engine)

## Content

- doc/ - documentation:
  - [HowTo install](doc/INSTALL.md)
  - [HowTo plugins](doc/Plugins.md)
  - [Apache web-server config sample](doc/doxgen.conf)
  - [Overwriting default settings sample](doc/local_settings.py)
- doxgen/ - project itself:
  - locale/ - Django std (i18n)
  - static/ - Django std
  - templates/ - Django std
  - misc/ - common useful things (utilities, templatetags etc...)
  - core/ - plugins management and converters
  - plugins/ - user defined plugins
  - udf/ - common user defined functions and references for all of plugins
  - *.py - Django std

## Contrib

- [django-templates-macros](https://github.com/twidi/django-templates-macros)
- [jquery](https://jquery.com/)
- [jquery.populate](https://github.com/dtuite/jquery.populate)
- [jquery.formset](https://gist.github.com/vandorjw/f884f0d51db3e7caaecd)
- [bytesize](https://github.com/danklammer/bytesize-icons) icons
