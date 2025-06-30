# TODO


## Issues:
- rm html preview (?)
- unify: 'html/xhtml' - the same
- Select engine in plugin; show/log engines loaded; preload engines
- PDF form: rm print.toml (use form field short names as HTML form names)
- `converter.py`: exceptions
- Plugins: main.py > json/toml/yaml (+pydantic) + README.md
- Refs as json (+pydantic)
- pathilb everywhere
- Deploy:
- + koji build chain
  + build for epel9 (py39) / epel10 (py..) / eln:
    * svglib (no reportlab)
    * rlPyCairo
    * .spec
  + copr for EPEL/ELN
- run LO headless constantly (use libreoffice-pyuno; RTFM unoconv)
- idea: engines as plugins (RTFM import.import_module)
- jinja2 (for compatibility)
- cache templates
- tests (speed too)
- rst doc
- async + await (?)
- nginx/unicorn etc
- Flask/aiohttp/FastAPI

## TODO
- exctract core into repo (templates/static/core); webserver/python web engine independent)
- pandoc:
  + html
  + odt
  + docx
  + Markdown
  + *LaTeX*
  + *RTF*
  + RML plugin

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
