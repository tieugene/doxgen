# Install
*(draft)*

Let's install into DESTDIR=/usr/share/doxgen:

1. install (one from):
   - ~~download and install rpm~~
   - download source from git, extract it into $DESTDIR + install Django
1. add requred backends depending on converters you want (see below)
1. create `$DESTDIR/local_settings.py` and `/etc/httpd/conf.d/doxgen.conf` (or wherever) like doc/* ones
1. create dir for sqlite DB (`mkdir /var/lib/doxgen`) ~~and MEDIA_ROOT~~
1. create DB (`cd $DESTDIR && python3 manage.py ...`)
1. assign owning and permissions:
   ```bash
   chown -R apache:apache {/etc/httpd/.../doxgen.conf,$DESTDIR,/var/lib/doxgen}
   chmod -R ...
   ```
1. let's go (`sudo systemctl start httpd`)

After this you can add your own plugins in $DESTDIR/plugins/ ([RTFM](Plugins.md))

## Converters (to PDF from):

- HTML (one from):
  - [weasyprint](https://github.com/Kozea/WeasyPrint) (py, pip, rpm, ~~brew~~)
  - [python-pdfkit](https://github.com/JazzCore/python-pdfkit) (py, pip, rpm, ~~brew~~)
    - &rdsh; [wkhtmltopdf](http://wkhtmltopdf.org/) (CLI, rpm, brew)
- RML:
  - [trml2pdf](https://github.com/JazzCore/python-pdfkit) (py, pip, *rpmable*, &lArr; reportlab)
- PDF form:
  - [jpype](https://github.com/jpype-project/jpype) (py, pip, rpm)
    - &rdsh; jre (openjdk8+; rpm, brew)
- *ODF: not tested yet, but will require libreoffice (core) --headless*

## Notes

Something concerning libreoffice-headless:
```bash
sudo mkdir /usr/share/httpd/.config
sudo chmod a+rwX /usr/share/httpd/.config
sudo chown -R apache:apache /usr/share/httpd/.config
sudo chown :apache /usr/share/httpd
sudo chmod g+w /usr/share/httpd
sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
```

