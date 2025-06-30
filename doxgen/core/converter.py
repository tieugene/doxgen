"""
Converters module.
Params:
    * template:str - path to template (.../*.html/fodf/rml)
    * context_dict: data
Returns: HttpResponse object

TODO: pagebreak, pagenum
"""

# 2. system
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import Iterable, Dict, Any, Tuple, Optional
# 2. django
from django.template import loader
# 3. 3rd party

TTF_DIR = pathlib.Path(__file__).parent.parent  / 'static' / 'ttf'

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
def __html2pdf_pdfkit(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """
    Render HTML to PDF using pdfkit+wkhtmltopdf
    :param context - dictionary of data
    :param template - path of tpl
    # TODO: dpi=300/600
    """
    try:
        import pdfkit
    except ModuleNotFoundError:
        return "'pdfkit' not found", None
    except ImportError as err:
        return "Error importing 'pdfkit': {}".format(err), None
    pdf = pdfkit.from_string(__render_template(template, context), False, options={'quiet': ''})
    if not pdf:
        return 'Something worng with pdfkit', None
    return '', pdf

def __html2pdf_weasy(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """
    Render HTML to PDF using weasyprint
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
    return '', weasyprint.HTML(string=__render_template(template, context)).write_pdf()

def __rml2pdf_trml(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """Convert RML to PDF using trml2pdf."""
    try:
        import trml2pdf
    except ModuleNotFoundError:
        return "'trml2pdf' not found", None
    except ImportError as err:
        return "Error importing 'trml2pdf': {}".format(err), None
    return '', trml2pdf.parseString(__render_template(template, context))

def __rml2pdf_z3c(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """Convert RML to PDF using zope-z3c.rml2pdf."""
    try:
        import z3c.rml.rml2pdf
    except ModuleNotFoundError:
        return "'z3c.rml' not found", None
    except ImportError as err:
        return "Error importing 'z3c.rml': {}".format(err), None
    # parseString returns BytesIO
    return '', z3c.rml.rml2pdf.parseString(__render_template(template, context)).read()

def __pdf2pdf_pypdfforms(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """
    Fill PDF form substituing data from rendered TOML template.
    @param template: toml-file
    @param context: [pdf form]
    """

    def __x_keys(__l: Iterable[str]) -> Dict[str, str]:
        """Create field translation dict[shot:str => full:str]."""

        def __clear_key(__s: str) -> str:
            """Clear field name:
            - head: rm like 'topmostSubform[0].Page1[0].'
            - tail: rm like '.[0]'
            """
            __tmp = __tmp1[-1] if (__tmp1 := __s.split('.')) else __s  # cut head
            return __tmp1[0] if (__tmp1 := __tmp.split('[')) else __tmp  # cut tail

        return {__clear_key(__k): __k for __k in __l}

    def __x_code(__data: Dict, __x: Dict[str, str]) -> Dict[str, Any]:
        return {__src_k: __v for __k, __v in __data.items() if (__src_k := __x.get(__k))}

    try:
        from PyPDFForm import PdfWrapper
        import tomllib
    except ModuleNotFoundError:
        return "'PyPDFForm' not found", None
    except ImportError as err:
        return "Error importing 'PyPDFForm': {}".format(err), None
    # 1. fill toml
    PdfWrapper.register_font('Arial', str(TTF_DIR / 'arial.ttf'))
    toml = __render_template(template, context)
    data = tomllib.loads(toml)
    # 2. convert keys
    form_file = template.rsplit('.', 1)[0] + '.pdf'       # must be alongside
    # 1.1. prepare real data
    form = PdfWrapper(form_file, global_font='Arial')
    fields = form.schema['properties']
    # __reg_fonts(reader)
    __x = __x_keys(fields.keys())
    data = __x_code(data, __x)
    # pprint.pprint(data)
    b = form.fill(data).read()
    return '', b

def __odt2pdf(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """
    Convert ODT to PDF using libreoffice-writer as server.
    sudo mkdir /usr/share/httpd/.config
    sudo chmod a+rwX /usr/share/httpd/.config
    sudo chown -R apache:apache /usr/share/httpd/.config
    sudo chown :apache /usr/share/httpd
    sudo chmod g+w /usr/share/httpd
    sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
    """
    if not shutil.which('libreoffice-writer'):
        return 'LibreOffice  Writer not found', None
    # 1. prepare
    tmp = tempfile.NamedTemporaryFile(suffix='.fodt', delete=True)  # delete=False to debug
    tmp.write(__render_template(template, context))
    tmp.flush()
    # 2. render
    tmp_dir = os.path.dirname(tmp.name)
    out_file = os.path.splitext(tmp.name)[0] + '.pdf'
    out, err = subprocess.Popen(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp_dir, tmp.name],
                                shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()
    # out, err = subprocess.Popen(['unoconv', '-f', 'pdf', '--stdout', tmp.name],...
    if err:
        data = None
    else:
        data = open(out_file, 'rb').read()
        os.remove(out_file)
    return err, data

__x2pdf = {  # extensions tuple, driver tupple
    'html': __html2pdf_weasy,
    'rml': __rml2pdf_trml,
    'toml': __pdf2pdf_pypdfforms,
    'fodt': __odt2pdf,
}

# ==== 3. Endpoints for external usage
def any2pdf(template: str, context: dict) -> Tuple[str, Optional[bytes]]:
    """
    EndPoint #2: Print
    :param template: full template path
    :param context: data
    :return: HttpResponse
    """
    ext = template.rsplit('.', 1)[1]
    return __x2pdf[ext](template, context)
