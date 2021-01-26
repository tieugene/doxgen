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
from django.utils.translation import gettext as _


# ==== 1. low-level utils (django dependent)
def __get_template_path(folder: str, template: str) -> str:
    """
    Get full template path
    :param folder: plugin folder
    :param template: template file name
    :return: Full template path
    """
    return os.path.join(folder, template)


def __render_template(template: str, context: dict) -> str:
    """
    Render template with data.
    :param template: template full path
    :param context: data
    :return: rendered
    Note: for fodt add context_type='text/xml'
    FIXME: loader.from_string()
    """
    return loader.get_template(template).render(context=context)


# ==== 2. renderers itself (independent)
def __html2pdf_pdfkit(template: str, context: dict) -> (str, bytes):
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)  # delete=False to debug
    pdfkit.from_string(__render_template(template, context), outfile.name, options={'quiet': ''})
    return '', outfile.read()


def __html2pdf_weasy(template: str, context: dict) -> (str, bytes):
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300
    """
    return '', weasyprint.HTML(string=__render_template(template, context)).write_pdf()


def __rml2pdf(template: str, context: dict) -> (str, bytes):
    return '', trml2pdf.doc.parse_string(__render_template(template, context))


def __xfdf2pdf_cli(template: str, context: dict) -> (str, bytes):
    """
    @param template: xfdf-file
    @param context: [pdf form]
    1. render xfdf to stdout
    2. merge pdf and stdin to stdout
    """
    pdf_tpl = template.rsplit('.', 1)[0] + '.pdf'
    out, err = subprocess.Popen(
        ['xfdftool', '-f', pdf_tpl],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate(__render_template(template, context))
    return err, out


def __xfdf2pdf_itext(template: str, context: dict) -> (str, bytes):
    # 1. fill xfdf
    pdf_tpl = os.path.join(settings.PLUGINS_DIR, template.rsplit('.', 1)[0] + '.pdf')
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
    return '', b


def __odf2pdf(template: str, context: dict) -> (bool, bytes):
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
    tmp.write(__render_template(template, context))
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


__x2pdf = {
    'htm': __html2pdf_weasy,
    'html': __html2pdf_weasy,
    'xhtm': __html2pdf_weasy,
    'xhtml': __html2pdf_weasy,
    'rml': __rml2pdf,
    'xfdf': __xfdf2pdf_itext,
    'fodt': __odf2pdf,
    'fods': __odf2pdf,
    'fodp': __odf2pdf,
}


# ==== 3. Endpoints for external usage
def html2html(folder: str, template: str, context: dict, as_attach: bool = False):
    """
    EndPint #1: Preview HTML template
    :param folder: plugin folder
    :param template: template file name (relative to plugin dir)
    :param context: data
    :param as_attach: view or download
    :return: HttpResponse
    """
    template_path = __get_template_path(folder, template)
    # ? +=; charset=UTF-8
    response = HttpResponse(content=__render_template(template_path, context), content_type='text/html')
    if as_attach:
        response['Content-Disposition'] = 'filename="print.html";'  # download: + ';attachment'
    return response


def any2pdf(folder: str, template: str, context: dict, as_attach: bool = False):
    """
    EndPoint #2: Print
    :param folder: plugin folder
    :param template: template file name (relative to plugin dir)
    :param context: data
    :param as_attach: view or download
    :return: HttpResponse
    """
    ext = template.rsplit('.', 1)[1]
    template_path = __get_template_path(folder, template)
    err, data = __x2pdf[ext](template_path, context)
    if err:
        response = HttpResponse(_('We had some errors:<pre>{}</pre>').format(err))
    else:
        response = HttpResponse(content=data, content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        if as_attach:
            response['Content-Disposition'] = 'filename="print.pdf";'  # download: + ';attachment'
    return response
