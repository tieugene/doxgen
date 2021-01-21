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

TODO: unlink from django (e.g. mk pure http reponse)
TODO: split on submodules:
bytes:__any2pdf(context: dict, template: str)
"""

# 2. system
import os
import subprocess
import tempfile
# 2. 3rd party
import pdfkit
import trml2pdf
# 3. django
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def __html2pdf_pdftk(request, context: dict, template) -> bytes:
    """
    Render [x]html to pdf
    :param context - dictionary of data
    :param template - path of tpl
    """
    # 1. prepare
    tmp = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=True)  # delete=False to debug
    tmp.write(render(request, template, context=context, content_type='text/xml').content)
    tmp.flush()
    outfile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=True)  # delete=False to debug
    # 2. render - new style
    # pdf = wkhtmltox.Pdf()
    # pdf.set_global_setting('out', outfile.name)
    # pdf.add_page({'page': 'file://%s' % os.path.abspath(tmp.name)})
    # pdf.convert()
    # 2. render - old style
    # TODO: replace w/ from_string
    # TODO: dpi=300
    pdfkit.from_file(tmp.name, outfile.name)
    return outfile.read()


def __rml2pdf(context: dict, template: str):
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


def __xfdf2pdf_itext(context: dict, template: str):
    # 1. fill xfdf
    pdf_tpl = os.path.join(settings.BASE_DIR, 'templates', template.rsplit('.', 1)[0] + '.pdf')
    xfdf = loader.get_template(template).render(context)
    # 2. gen pdf
    import jpype.imports
    if isinstance(xfdf, str):
        xfdf = bytes(xfdf, 'UTF-8')
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['jars/*'])
    from com.itextpdf.text.pdf import PdfReader, PdfStamper, XfdfReader
    from java.io import ByteArrayInputStream, ByteArrayOutputStream
    pdf_reader = PdfReader(pdf_tpl)     # (filename:str|byte[]|InputStream)
    o_str = ByteArrayOutputStream()
    stamper = PdfStamper(pdf_reader, o_str)
    stamper.setFormFlattening(True)
    stamper.getAcroFields().setFields(XfdfReader(ByteArrayInputStream(xfdf)))
    stamper.close()
    b = bytes(o_str.toByteArray())   # java byte[]
    # jpype.shutdownJVM()
    return b


# ====
def html2html(request, context: dict, template: str):
    return render(request, template, context=context)


def html2pdf(request, context: dict, template: str):
    data = __html2pdf_pdftk(request, context, template)
    response = HttpResponse(content=data, content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    # response['Content-Disposition'] = 'filename=\"print.pdf\";'     # download: + ';attachment'
    # 4. cleanup
    # if (os.path.exists(outfile.name)):
    #    os.remove(outfile.name)	# hack
    return response


def rml2pdf(_, context: dict, template: str):
    """
    Create pdf from rml-template and return file to user
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    # response['Content-Disposition'] = 'attachment; filename="print.pdf";'
    response.write(__rml2pdf(context, template))
    # response.write(tpl.render(tc).encode('utf-8'))
    return response


def xfdf2pdf(_, context: dict, template: str):
    data = __xfdf2pdf_itext(context, template)
    if not data:
        # response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
        response = HttpResponse('We had some errors:<pre>%s</pre>' % err + pdftpl)
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        # response['Content-Disposition'] = 'attachment; filename=\"print.pdf\";'
        response.write(data)
    return response


def odf2pdf(request, context: dict, template: str):
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
    tmp.write(render(request, template, context=context_dict, content_type='text/xml').content)
    tmp.flush()
    # 2. render
    tmp_dir = os.path.dirname(tmp.name)
    out_file = os.path.splitext(tmp.name)[0] + '.pdf'
    out, err = subprocess.Popen(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp_dir, tmp.name],
                                shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    # out, err = subprocess.Popen(['unoconv', '-f', 'pdf', '--stdout', tmp.name],...
    if err:
        response = HttpResponse('We had some errors:<pre>%s</pre>' % err)
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        response['Content-Disposition'] = 'attachment; filename=\"print.pdf\";'
        response.write(open(out_file).read())
        os.remove(out_file)
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
