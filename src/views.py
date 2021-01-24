# -*- coding: utf-8 -*-

# 1. system
import logging
from collections import OrderedDict
# 2. 3rd party
# 3. django
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
# 4. my
# from misc.utils import eprint
from core.consts import *
import core.converter
import core.mgr
import forms

logger = logging.getLogger(__name__)
PAGE_SIZE = 20


def __log_request(request):
    """
    .method == .META['REQUEST_METHOD']
    .encoding == None
    .path_info == .META['PATH_INFO']

    Payload: data=json.dumps(meta, indent=1, ensure_ascii=False)
    meta = request.META
    for k in meta.keys():
        if k.islower():
            del (meta[k])
    """
    # if not settings.DEBUG:
    logger.info(
        "Method={}, IP={}, Path={}, Agent={}".format(
            request.META['REQUEST_METHOD'],
            request.META['REMOTE_ADDR'],
            request.META['PATH_INFO'][:254],
            request.META.get('HTTP_USER_AGENT', 'noname')[:254]
        )
    )


def try_tpl(fn):
    def _wrapped(*args, **kwargs):
        core.mgr.try_load_plugins(settings.PLUGINS_DIR, forms.GenForm, forms.GenFormSets)
        return fn(*args, **kwargs)

    return _wrapped


# ====
class TplList(TemplateView):
    template_name = "tpl_list.html"

    @try_tpl
    def get_context_data(self, **kwargs):
        # __log_request(request)
        context = super().get_context_data(**kwargs)
        context['data'] = core.mgr.moduledict
        return context


@try_tpl
def doc_a(request, uuid):
    """
    Anon/Create/Update
    :param request:
    :param uuid:str - uuid (anon/create) or doc id (update)
    :return request, html_tpl_name, context:dict
    """
    __log_request(request)
    tpl = core.mgr.moduledict[uuid]
    # 1. check <pkg>.ANON/CREATE/UPDATE
    self_func = [K_T_F_ANON, K_T_F_ADD, K_T_F_EDIT][0]  # mode=0 (anon) => PRINT
    if self_func in tpl[K_V_MODULE].__dict__:
        return tpl[K_V_MODULE].__dict__[self_func](request, uuid)  # uuid was pk
    # 2. get FORM and FORMSETS
    formclass = tpl[K_T_FORM]
    formsetsclass = tpl[K_T_FORMSETS]  # OrderedDict of dicts
    if request.method == 'POST':
        form = formclass(request.POST)
        del form.fields[K_T_F_NAME]  # if mode == 0:  # ANON, Create/Update -> view/print
        formlist = OrderedDict()
        isvalid = form.is_valid()
        for k, formset in formsetsclass.items():
            formlist[k] = formset(request.POST, prefix=k)
            isvalid = isvalid and formlist[k].is_valid()
        if isvalid:
            data = form.cleaned_data
            # inject formsets into data
            for k, v in formlist.items():
                dataset = list()
                for i in v.cleaned_data:  # list of dicts
                    if i:  # reject empty dicts
                        dataset.append(i)
                if dataset:  # reject empty lists
                    data[k] = dataset  # inject datasets into data
            core.mgr.try_to_call(tpl, K_T_F_POST_FORM, data)
            # split
            # if mode == 0:  # ANON > PRINT, C/U -> V/P
            if (K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_PRINT in tpl[K_V_MODULE].DATA[K_T_T]):
                context_dict = {'data': data}
                template = tpl[K_V_MODULE].DATA[K_T_T][K_T_T_PRINT]
                if request.POST.get('_action', None) == 'view':
                    core.mgr.try_to_call(tpl, K_T_F_PRE_VIEW, data)  # Create/Update -> View
                    return core.converter.html2html(tpl[K_T_DIR], template, context_dict)
                else:  # Anon/Create/Update -> PRINT
                    core.mgr.try_to_call(tpl, K_T_F_PRE_PRINT, data)
                    return core.converter.any2pdf(tpl[K_T_DIR], template, context_dict)
            else:  # tmp dummy
                return redirect('tpl_list')
    else:  # GET
        form = formclass()
        del form.fields[K_T_F_NAME]
        formlist = OrderedDict()
        for k, formset in formsetsclass.items():
            formlist[k] = formset(prefix=k)
    form_template = tpl[K_T_DIR] + '/' + tpl[K_V_MODULE].DATA[K_T_T][K_T_T_FORM]\
        if ((K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_FORM in tpl[K_V_MODULE].DATA[K_T_T]))\
        else 'auto_form.html'
    return render(
        request,
        form_template,
        context={
            'name': tpl[K_V_MODULE].DATA[K_T_NAME],
            'comments': tpl[K_V_MODULE].DATA.get(K_T_COMMENTS, ''),
            'legend': tpl[K_V_MODULE].DATA.get(K_T_LEGEND, ''),
            'uuid': tpl[K_V_MODULE].DATA[K_T_UUID],
            'form': form,
            'formlist': formlist,
            'example': tpl[K_V_MODULE].DATA.get('example', None),
        })
