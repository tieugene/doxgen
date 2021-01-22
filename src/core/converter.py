"""
Converters module
Params:
    * request: request
    * context_dict: data
    * template:str - path to template (.../*.html/fodf/rml)
Returns: HttpResponse object

Input:
    * [x]htm[l] => [html/]pdf
    * rml => pdf
    * fodf => pdf/*
Try:
    * lyx => pdf (too long; lyx -e)
    * svg (webkit, inkscape (pyqt))
    * scribus (pyqt) - don't know
    * html5 (webkit)
    * pdf forms (pdftk)

FIXME: __...() -> (err, bytes)
TODO: unlink from django (e.g. mk pure http reponse)
TODO: split on submodules: bytes:__any2pdf(context: dict, template: str)
TODO: dispatcher(tpl_type:str) -> func
TODO: pagebreak, pagenum
Note: add static: content => tc={'STATIC_ROOT': settings.STATIC_ROOT}; tc.update(content)
"""

# 2. system
import os
import subprocess
import tempfile
# 2. 3rd party
import pdfkit
import trml2pdf
import weasyprint
# 3. django
from django.conf import settings
from django.http import HttpResponse
from django.template import loader


def __html2html(context: dict, template: str) -> str:
    return loader.get_template(template).render(context)


def __html2pdf_pdfkit(context: dict, template: str) -> bytes:
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)  # delete=False to debug
    pdfkit.from_string(loader.get_template(template).render(context), outfile.name, options={'quiet': ''})
    return outfile.read()


def __html2pdf_weasy(context: dict, template: str) -> bytes:
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    return weasyprint.HTML(string=loader.get_template(template).render(context)).write_pdf()


def __rml2pdf(context: dict, template: str) -> bytes:
    tpl = loader.get_template(template)
    tc = {'STATIC_ROOT': settings.STATIC_ROOT}
    tc.update(context)
    return trml2pdf.parseString(tpl.render(tc).encode('utf-8'))


def __xfdf2pdf_cli(context: dict, template: str) -> bytes:
    """
    @param template: xfdf-file
    @param context: [pdf form]
    1. render xfdf to stdout
    2. merge pdf and stdin to stdout
    """
    pdftpl = os.path.join(settings.BASE_DIR, 'templates', template.rsplit('.', 1)[0] + '.pdf')
    out, err = subprocess.Popen(
        ['xfdftool', '-f', pdftpl],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate(str(loader.get_template(template).render(context)))
    return None if err else out


def __xfdf2pdf_itext(context: dict, template: str) -> bytes:
    # 1. fill xfdf
    pdf_tpl = os.path.join(settings.BASE_DIR, 'templates', template.rsplit('.', 1)[0] + '.pdf')
    xfdf = loader.get_template(template).render(context)
    # 2. gen pdf
    import jpype.imports
    if isinstance(xfdf, str):
        xfdf = bytes(xfdf, 'UTF-8')
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['core/jars/*'])
    from com.itextpdf.text.pdf import PdfReader, PdfStamper, XfdfReader
    from java.io import ByteArrayInputStream, ByteArrayOutputStream
    pdf_reader = PdfReader(pdf_tpl)  # (filename:str|byte[]|InputStream)
    o_str = ByteArrayOutputStream()
    stamper = PdfStamper(pdf_reader, o_str)
    stamper.setFormFlattening(True)
    stamper.getAcroFields().setFields(XfdfReader(ByteArrayInputStream(xfdf)))
    stamper.close()
    b = bytes(o_str.toByteArray())  # java byte[]
    # jpype.shutdownJVM()
    return b


def __odf2pdf(context: dict, template: str) -> (bool, bytes):
    """
    sudo mkdir /usr/share/httpd/.config
    sudo chmod a+rwX /usr/share/httpd/.config
    sudo chown -R apache:apache /usr/share/httpd/.config
    sudo chown :apache /usr/share/httpd
    sudo chmod g+w /usr/share/httpd
    sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
    """
    # 1. prepare
    tmp = tempfile.NamedTemporaryFile(suffix='.fodt', delete=True)  # delete=False to debug
    tmp.write(loader.get_template(template).render(context=context, content_type='text/xml').content)
    tmp.flush()
    # 2. render
    tmp_dir = os.path.dirname(tmp.name)
    out_file = os.path.splitext(tmp.name)[0] + '.pdf'
    out, err = subprocess.Popen(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp_dir, tmp.name],
                                shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # out, err = subprocess.Popen(['unoconv', '-f', 'pdf', '--stdout', tmp.name],...
    if err:
        data = None
    else:
        data = open(out_file).read()
        os.remove(out_file)
    return err, data


# ====
def html2html(_, context: dict, template: str, as_attach: bool = False):
    response = HttpResponse(content=__html2html(context, template), content_type='text/html')  # ; charset=UTF-8
    if as_attach:
        response['Content-Disposition'] = 'filename="print.html";'  # download: + ';attachment'
    return response


def html2pdf(_, context: dict, template: str, as_attach: bool = False):
    data = __html2pdf_weasy(context, template)
    response = HttpResponse(content=data, content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    if as_attach:
        response['Content-Disposition'] = 'filename="print.pdf";'  # download: + ';attachment'
    return response


def rml2pdf(_, context: dict, template: str, as_attach: bool = False):
    """
    Create pdf from rml-template and return file to user
    """
    data = __rml2pdf(context, template)
    response = HttpResponse(content=data, content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    if as_attach:
        response['Content-Disposition'] = 'attachment; filename="print.pdf";'
    return response


def xfdf2pdf(_, context: dict, template: str, as_attach: bool = False):
    data = __xfdf2pdf_itext(context, template)
    if not data:
        # response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
        response = HttpResponse('We had some errors:<pre>%s</pre>' % template)
    else:
        response = HttpResponse(content=data, content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        if as_attach:
            response['Content-Disposition'] = 'attachment; filename="print.pdf";'
    return response


def odf2pdf(_, context: dict, template: str, as_attach: bool = False):
    """
    sudo mkdir /usr/share/httpd/.config
    sudo chmod a+rwX /usr/share/httpd/.config
    sudo chown -R apache:apache /usr/share/httpd/.config
    sudo chown :apache /usr/share/httpd
    sudo chmod g+w /usr/share/httpd
    sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
    """
    err, data = __odf2pdf(context, template)
    if err:
        response = HttpResponse('We had some errors:<pre>%s</pre>' % err)
    else:
        response = HttpResponse(content=data, content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        if as_attach:
            response['Content-Disposition'] = 'attachment; filename="print.pdf";'
    return response


x2pdf = {
    'htm': html2pdf,
    'html': html2pdf,
    'xhtm': html2pdf,
    'xhtml': html2pdf,
    'rml': rml2pdf,
    'xfdf': xfdf2pdf,
    'fodt': odf2pdf,
    'fods': odf2pdf,
    'fodp': odf2pdf,
}
