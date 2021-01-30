"""
Converters module
Params:
    * template:str - path to template (.../*.html/fodf/rml)
    * context_dict: data
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

TODO: pagebreak, pagenum
"""

# 2. system
import os
import subprocess
import tempfile
# 2. 3rd party
# On demand:
# - pdfkit
# - weasyprint
# - trml2pdf
# - jpype
# 3. django
from django.template import loader


# ==== 1. low-level utils (django dependent)
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
    try:
        import pdfkit
    except ModuleNotFoundError:
        return "'pdfkit' not found", None
    except ImportError as err:
        return "Error importing 'pdfkit': {}".format(err), None
    except Exception as err:
        return "Unknown error importing 'pdfkit': {}".format(err), None
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
    try:
        import weasyprint
    except ModuleNotFoundError:
        return "'weasyprint' not found", None
    except ImportError as err:
        return "Error importing 'weasyprint': {}".format(err), None
    except Exception as err:
        return "Unknown error importing 'weasyprint': {}".format(err), None
    return '', weasyprint.HTML(string=__render_template(template, context)).write_pdf()


def __rml2pdf(template: str, context: dict) -> (str, bytes):
    try:
        import trml2pdf
    except ModuleNotFoundError:
        return "'trml2pdf' not found", None
    except ImportError as err:
        return "Error importing 'trml2pdf': {}".format(err), None
    except Exception as err:
        return "Unknown error importing 'trml2pdf': {}".format(err), None
    return '', trml2pdf.parseString(__render_template(template, context))


def __xfdf2pdf_cli(template: str, context: dict) -> (str, bytes):
    """
    @param template: xfdf-file
    @param context: [pdf form]
    1. render xfdf to stdout
    2. merge pdf and stdin to stdout
    """
    pdf_tpl = template.rsplit('.', 1)[0] + '.pdf'       # must be alongside
    out, err = subprocess.Popen(
        ['xfdftool', '-f', pdf_tpl],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate(__render_template(template, context))
    return err, out


def __xfdf2pdf_itext(template: str, context: dict) -> (str, bytes):
    try:
        import jpype.imports
    except ModuleNotFoundError:
        return "'jpype' not found", None
    except ImportError as err:
        return "Error importing 'jpype': {}".format(err), None
    except Exception as err:
        return "Unknown error importing 'jpype': {}".format(err), None
    # 1. fill xfdf
    pdf_tpl = template.rsplit('.', 1)[0] + '.pdf'       # must be alongside
    xfdf = __render_template(template, context)
    # 2. gen pdf
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
def html2html(template: str, context: dict) -> str:
    """
    EndPint #1: Preview HTML template
    :param template: full template path
    :param context: data
    :return: HttpResponse
    """
    # ? +=; charset=UTF-8
    return __render_template(template, context)


def any2pdf(template: str, context: dict):
    """
    EndPoint #2: Print
    :param template: full template path
    :param context: data
    :return: HttpResponse
    """
    ext = template.rsplit('.', 1)[1]
    return __x2pdf[ext](template, context)
