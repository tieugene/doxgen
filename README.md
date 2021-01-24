# DoxGen

Document generator

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

----
## 2. Features:
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
  - plugins/*/ - plugins
