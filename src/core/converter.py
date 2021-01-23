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
"""

# 2. system
import os
import subprocess
import tempfile
# 2. 3rd party
import pdfkit
import trml2pdf.doc
import weasyprint
# 3. django
from django.conf import settings
from django.http import HttpResponse
from django.template import loader


# ==== 1. low-level utils (django dependent)
def __get_template(template: str, ext: str) -> str:
    """
    Get new template based on exists and extension
    :param template:
    :param ext:
    :return:
    """
    return os.path.join(settings.BASE_DIR, 'templates', template.rsplit('.', 1)[0] + '.' + ext)


def __render_template(template: str, context: dict) -> str:
    """
    Render template with data.
    :param template:
    :param context:
    :return:
    Note: for fodt add context_type='text/xml'
    """
    return loader.get_template(template).render(context=context)


def __response_pdf(data: bytes, as_attach: bool):
    response = HttpResponse(content=data, content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    if as_attach:
        response['Content-Disposition'] = 'filename="print.pdf";'  # download: + ';attachment'
    return response


# ==== 2. renderers itself (independent)
def __html2html(context: dict, template: str) -> str:
    return __render_template(template, context)


def __html2pdf_pdfkit(context: dict, template: str) -> bytes:
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)  # delete=False to debug
    pdfkit.from_string(__render_template(template, context), outfile.name, options={'quiet': ''})
    return outfile.read()


def __html2pdf_weasy(context: dict, template: str) -> bytes:
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    return weasyprint.HTML(string=__render_template(template, context)).write_pdf()


def __rml2pdf(context: dict, template: str) -> bytes:
    return trml2pdf.doc.parse_string(__render_template(template, context))


def __xfdf2pdf_cli(context: dict, template: str) -> bytes:
    """
    @param template: xfdf-file
    @param context: [pdf form]
    1. render xfdf to stdout
    2. merge pdf and stdin to stdout
    """
    pdf_tpl = __get_template(template, 'pdf')
    out, err = subprocess.Popen(
        ['xfdftool', '-f', pdf_tpl],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate(__render_template(template, context))
    return None if err else out


def __xfdf2pdf_itext(context: dict, template: str) -> bytes:
    # 1. fill xfdf
    pdf_tpl = __get_template(template, 'pdf')
    xfdf = __render_template(template, context)
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
    tmp.write(__render_template(template, context).content)
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


# ==== 3. Wrappers for external usage
def html2html(context: dict, template: str, as_attach: bool = False):
    response = HttpResponse(content=__html2html(context, template), content_type='text/html')  # ; charset=UTF-8
    if as_attach:
        response['Content-Disposition'] = 'filename="print.html";'  # download: + ';attachment'
    return response


def html2pdf(context: dict, template: str, as_attach: bool = False):
    data = __html2pdf_weasy(context, template)
    return __response_pdf(data, as_attach)


def rml2pdf(context: dict, template: str, as_attach: bool = False):
    """
    Create pdf from rml-template and return file to user
    """
    data = __rml2pdf(context, template)
    return __response_pdf(data, as_attach)


def xfdf2pdf(context: dict, template: str, as_attach: bool = False):
    data = __xfdf2pdf_itext(context, template)
    if not data:
        # response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
        response = HttpResponse('We had some errors:<pre>%s</pre>' % template)
    else:
        response = __response_pdf(data, as_attach)
    return response


def odf2pdf(context: dict, template: str, as_attach: bool = False):
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
        response = __response_pdf(data, as_attach)
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
