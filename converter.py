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
TODO: split on submodules
"""

# 2. system
import os
import subprocess
import tempfile
# 3. 3rd party
# html
import pdfkit
# rml
import trml2pdf
# 1. django
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# odf - cli (unoconv)
# pdf - cli (xfdftool)


def html2html(request, context_dict, template):
    return render(request, template, context=context_dict)


def html2pdf(request, context_dict, template):
    """
    Render [x]html to pdf
    :param request - request
    :param context_dict - dictionary of data
    :param template - path of tpl
    """
    # 1. prepare
    tmp = tempfile.NamedTemporaryFile(suffix='.xhtml', delete=True)  # delete=False to debug
    tmp.write(render(request, template, context=context_dict, content_type='text/xml').content)
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
    # 3. response
    response = HttpResponse(content=outfile.read(), content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    # response['Content-Disposition'] = 'filename=\"print.pdf\";'     # download: + ';attachment'
    # 4. cleanup
    # if (os.path.exists(outfile.name)):
    #    os.remove(outfile.name)	# hack
    return response


def rml2pdf(_, context_dict, template):
    """
    Create pdf from rml-template and return file to user
    """
    response = HttpResponse(mimetype='application/pdf', content_type='application/pdf')
    response['Content-Transfer-Encoding'] = 'binary'
    response['Content-Disposition'] = 'attachment; filename=\"print.pdf\";'
    tpl = loader.get_template(template)
    tc = {'STATIC_ROOT': settings.STATIC_ROOT}
    tc.update(context_dict)
    response.write(trml2pdf.parseString(tpl.render(tc).encode('utf-8')))
    # response.write(tpl.render(tc).encode('utf-8'))
    return response


def xfdf2pdf(_, context_dict, template):
    """
    @param _: not used
    @param template: xfdf-file
    @param context_dict: [pdf form]
    1. render xfdf to stdout
    2. merge pdf and stdin to stdout
    """
    pdftpl = os.path.join(settings.BASE_DIR, 'templates', template.rsplit('.', 1)[0] + '.pdf')
    out, err = subprocess.Popen(['xfdftool', '-f', pdftpl], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate(
        str(loader.get_template(template).render(context_dict)))
    if err:
        # response = HttpResponse('We had some errors:<pre>%s</pre>' % escape(err) + pdftpl)
        response = HttpResponse('We had some errors:<pre>%s</pre>' % err + pdftpl)
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Transfer-Encoding'] = 'binary'
        response['Content-Disposition'] = 'attachment; filename=\"print.pdf\";'
        response.write(out)
    return response


def odf2pdf(request, context_dict, template):
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
