# TODO


## Issues:
- PDF form: iText+XFDF => python+TOML
- `converter.py`: exceptions
- pathilb everywhere
- Plugins: main.py > json/toml/yaml (|pydantic) + README.md
- unify: 'html/xhtml' - the same
- Select engine in plugin; show/log engines loaded; preload engines
- Preview PDF in browser
- rm html preview (?)
- idea: converters (engines) as plugins (RTFM import.import_module)
- use jinja2 (for compatibility)
- tests (speed too)
- rst doc
- async + wait
- nginx/unicorn etc
- aiohttp/Flask/FastAPI
- cache templates
- rm print.toml for PDF (use form field short names as HTML form names)
- pandoc:
   + Markdown
   + LaTeX
   + RTF

## TODO
- no java (pure python)
- build for epel9 (python 3.9):
  + svglib (no reportlab)
  + rlPyCairo
- koji build chain
- FIXME: run LO headless constantly (use libreoffice-pyuno; RTFM unoconv)
- exctract core into repo (templates/static/core); webserver/python web engine independent)
- try pandoc (html/odt/docx/md)
- copr repo for epel9

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
