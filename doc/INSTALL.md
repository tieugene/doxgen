# Install
*(draft)*

Let's install into DESTDIR=/usr/share/doxgen:

1. install (one from):
   - ~~download and install rpm~~
   - download source from git, extract it into $DESTDIR + install python3-django, python3-mod_wsgi
1. add requred backends depending on converters you want (see below)
1. create `$DESTDIR/local_settings.py` like doc/* one
1. create `/etc/httpd/conf.d/doxgen.conf` (or wherever) like doc/* one
1. create dir for sqlite DB (`mkdir /var/lib/doxgen`) ~~and MEDIA_ROOT~~
1. create DB:
   ```bash
   cd $DESTDIR
   python3 manage.py migrate
   python3 manage.py createsuperuser --username admin --email admin@exmaple.com --noinput
   python3 manage.py changepassword admin
   ```
1. assign owning and permissions:
   ```bash
   chown -R apache:apache {/etc/httpd/.../doxgen.conf,$DESTDIR/plugins,/var/lib/doxgen}
   # chmod -R ...
   ```
1. let's go: `sudo systemctl start httpd`

After this you can add your own plugins in $DESTDIR/plugins/ ([RTFM](Plugins.md))

## Converters (to PDF from):

- HTML (one from):
  - [weasyprint](https://github.com/Kozea/WeasyPrint) (py, pip, rpm, ~~brew~~)
  - [python-pdfkit](https://github.com/JazzCore/python-pdfkit) (py, pip, rpm, ~~brew~~)
    - &rdsh; [wkhtmltopdf](http://wkhtmltopdf.org/) (CLI, rpm, brew)
  - [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) (py, pip, *rpmable*, ~~brew~~; [notes](http://dik123.blogspot.com/2009/02/html-pdf.html) for non-ascii)
- RML (one from):
  - [trml2pdf](https://github.com/romanlv/trml2pdf) (py, pip, *rpmable*, &lArr; reportlab)
  - [z3c.rml](https://github.com/zopefoundation/z3c.rml) (py, pip, *rpmable*, &lArr; reportlab)
- PDF form:
  - [jpype](https://github.com/jpype-project/jpype) (py, pip, rpm)
    - &rdsh; jre (openjdk8+; rpm, brew)
- *ODF: not tested yet, but will require libreoffice (core) --headless*

## Notes

Note 1: html for xhtmls2pdf (url(font)) incompatible with pdfkit (network error)!
```css
    @font-face {
        font-family: Arial;
        src: url(arial.ttf);
    }
    @font-face {
        font-family: Times;
        src: url(times.ttf);
    }
```

Something concerning libreoffice-headless:
```bash
sudo mkdir /usr/share/httpd/.config
sudo chmod a+rwX /usr/share/httpd/.config
sudo chown -R apache:apache /usr/share/httpd/.config
sudo chown :apache /usr/share/httpd
sudo chmod g+w /usr/share/httpd
sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
```
&hellip;
