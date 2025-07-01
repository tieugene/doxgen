# TODO


## Issues:
- pathlib everywhere
- JSONify:
  + Plugins: main.py > [main.py +] json/toml/yaml (+pydantic) + JSON schema + README.md 
  + udf/* as json (+pydantic)
  + consts.py: enums
- Django templates => jinja2
- run LO headless constantly (use libreoffice-pyuno; RTFM unoconv)
- FIXME: pdfkit
- Deploy:
  + pylint, reformat
  + pyproject .toml
  + .spec
  + koji build chain
  + build for epel9 (py39) / epel10 (py..) / eln:
    * svglib (no reportlab)
    * rlPyCairo
  + copr for EPEL/ELN
  + rst doc
  + tests (speed too)
- Multiplatform:
  + engines as plugins (RTFM import.import_module)
  + Flask/aiohttp/FastAPI/cherrypy
  + nginx/unicorn etc

## Ideas
- move to CentOs Steam 10
- exctract core into repo (templates/static/core); webserver/python web engine independent)
- pandoc:
  + html
  + odt
  + docx
  + Markdown
  + *LaTeX*
  + *RTF*
  + RML plugin
- HTML5:
  + input limits (size, maxlength, ...)
  + input types (tel, date, email, ...)
- cache plugin templates

## Depricated:
- html:
  + ~~xhtml2pdf~~
- pdf:
  + [~~pdfforms~~](https://github.com/altaurog/pdfforms) (pdftk-java)
  + ~~iText~~
  + ~~qpdf~~
  + [xfdf-merger](https://github.com/itext/xfdf-merger)
  + [itext-python](https://github.com/itext/itext-python-example): html2pdf too
  + [~~pypdf~~](https://pypdf.readthedocs.io/en/stable/user/forms.html)
