"""
Converters module.
Params:
    * template:str - path to template (.../*.html/fodf/rml)
    * context_dict: data
Returns: HttpResponse object

TODO: pagebreak, pagenum
TODO: framework-independent
TODO: In: context, plugin_dir[, ext]
"""
# 1. system
import pathlib
import shutil
import subprocess
import tempfile
import tomllib
import logging
from typing import Iterable, Dict, Any
# 2. django
from django.template import loader
# 3. 3rd party
# 4. self
from .exc import DGRenderExc

try:
    import pdfkit  # Note: install wkhtmltopdf
except (ModuleNotFoundError, ImportError) as e:
    logging.error("%s: %s", __name__, e)  # ModuleNotFoundError: No module named 'something'
try:
    import weasyprint
except (ModuleNotFoundError, ImportError) as e:
    logging.error("%s: %s", __name__, e)  # ModuleNotFoundError: No module named 'something'
try:
    import trml2pdf
except (ModuleNotFoundError, ImportError) as e:
    logging.error("%s: %s", __name__, e)  # ModuleNotFoundError: No module named 'something'
try:
    import z3c.rml.rml2pdf
except (ModuleNotFoundError, ImportError) as e:
    logging.error("%s: %s", __name__, e)  # ModuleNotFoundError: No module named 'something'
try:
    import PyPDFForm
    TTF_DIR = pathlib.Path(__file__).parent.parent / 'static' / 'ttf'
    PyPDFForm.PdfWrapper.register_font('Arial', str(TTF_DIR / 'arial.ttf'))
except (ModuleNotFoundError, ImportError) as e:
    logging.error("%s: %s", __name__, e)  # ModuleNotFoundError: No module named 'something'

x2pdf = {}

# ==== 1. low-level utils (django dependent)
def __render_template(template: pathlib.Path, context: dict) -> str:
    """
    Render template with data.
    :param template: template full path
    :param context: data
    :return: rendered
    Note: for fodt add context_type='text/xml'
    FIXME: loader.from_string()
    """
    return loader.get_template(str(template)).render(context=context)

# ==== 2. renderers itself (independent)
def __html2pdf_pdfkit(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """
    Render HTML to PDF using pdfkit+wkhtmltopdf
    :param context - dictionary of data
    :param plugin_dir: plugin full path
    # TODO: dpi=300/600
    """
    if pdf := pdfkit.from_string(__render_template(plugin_dir / 'print.html', context), False,
                                 options={'quiet': ''}):
        return pdf
    else:
        raise DGRenderExc('Something worng with pdfkit')

def __html2pdf_weasy(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """
    Render HTML to PDF using weasyprint
    :param context - dictionary of data
    :param plugin_dir: plugin full path
    # TODO: dpi=300
    """
    return weasyprint.HTML(string=__render_template(plugin_dir / 'print.html', context)).write_pdf()

def __rml2pdf_trml(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """Convert RML to PDF using trml2pdf."""
    return trml2pdf.parseString(__render_template(plugin_dir / 'print.rml', context))

def __rml2pdf_z3c(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """Convert RML to PDF using zope-z3c.rml2pdf."""
    return z3c.rml.rml2pdf.parseString(__render_template(plugin_dir / 'print.rml', context)).read()

def __pdf2pdf_pypdfforms(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """
    Fill PDF form substituing data from rendered TOML template.
    :param context: [pdf form]
    :param plugin_dir: plugin full path
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

    # 1. fill toml
    toml = __render_template(plugin_dir / 'print.toml', context)
    data = tomllib.loads(toml)
    # 2. convert keys
    # 1.1. prepare real data
    form = PyPDFForm.PdfWrapper(str(plugin_dir / 'print.pdf'), global_font='Arial')
    fields = form.schema['properties']
    __x = __x_keys(fields.keys())
    data = __x_code(data, __x)
    return form.fill(data).read()

def __odt2pdf(context: dict, plugin_dir: pathlib.Path) -> bytes:
    """
    Convert ODT to PDF using libreoffice-writer as server.
    :param plugin_dir: plugin full path
    sudo mkdir /usr/share/httpd/.config
    sudo chmod a+rwX /usr/share/httpd/.config
    sudo chown -R apache:apache /usr/share/httpd/.config
    sudo chown :apache /usr/share/httpd
    sudo chmod g+w /usr/share/httpd
    sudo -u apache libreoffice --headless --convert-to pdf --outdir /tmp /tmp/test.fodt
    """
    # 1. prepare
    tmp = tempfile.NamedTemporaryFile(suffix='.fodt', delete=True)  # delete=False to debug
    tmp.write(__render_template(plugin_dir / 'print.fodt', context))
    tmp.flush()
    tmp_file = pathlib.Path(tmp.name)
    # 2. render
    tmp_dir = tmp_file.parent
    out_file = tmp_file.with_suffix('.pdf')
    out, err = subprocess.Popen(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp_dir, tmp_file],
                                shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()
    # out, err = subprocess.Popen(['unoconv', '-f', 'pdf', '--stdout', tmp.name],...
    if err:
        raise DGRenderExc('Something worng with odt')
    else:
        data = out_file.open('rb').read()
        out_file.unlink()
        return data

def __preload():
    globs = globals()
    if 'pdfkit' in globs:
        x2pdf['pdfkit'] = __html2pdf_pdfkit
        logging.info("'pdfkit' plugin loaded.")
    if 'weasyprint' in globs:
        x2pdf['weasy'] = __html2pdf_weasy
        logging.info("'weasy' plugin loaded.")
    if 'trml2pdf' in globs:
        x2pdf['trml2pdf'] = __rml2pdf_trml
        logging.info("'trml2pdf' plugin loaded.")
    if 'z3c' in globs:
        x2pdf['z3c.rml'] = __rml2pdf_z3c
        logging.info("'z3c.rml' plugin loaded.")
    if 'PyPDFForm' in globs:
        x2pdf['pypdfform'] = __pdf2pdf_pypdfforms
        logging.info("'pypdfform' plugin loaded.")
    # odt
    if not shutil.which('oowriter'):
        logging.warning( 'LibreOffice  Writer not found')
    else:
        x2pdf['odt'] = __odt2pdf
        logging.info("'odt' plugin loaded.")

__preload()
