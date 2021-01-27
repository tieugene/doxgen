# DoxGen

DoxGen - an application to fill out and print template documents.<br/>
Template formats: HTML, [RML](https://www.reportlab.com/docs/rml-for-idiots.pdf), PDF forms, [ODF](https://en.wikipedia.org/wiki/OpenDocument).<br/>
Output: HTML, PDF.

## Advantages:

- Simple templates rendering into output document HTML templating
- High-quality final PDF for predictable printing result
- Extending user defined template set using simple plugins subsystem
- Support most popular document formats as templates

## Content

- doc/ - documentation:
  - [HowTo install](doc/INSTALL.md)
  - [HowTo make plugins](doc/Plugins.md)
  - [doxgen.conf](doc/doxgen.conf) sample for Apache web-server
  - [local_setting.py](doc/local_setting.py) sample to overwrite default settings
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

Bundled artifacts:

- [django-templates-macros](https://github.com/twidi/django-templates-macros)
- [jquery](https://jquery.com/)
- [jquery.populate](https://github.com/dtuite/jquery.populate)
- jquery.formset (source forgotten)
- [bytesize](https://github.com/danklammer/bytesize-icons) icons
- [itextpdf](https://github.com/itext/itextpdf) 5.5.13.2
