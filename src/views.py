# -*- coding: utf-8 -*-

# 1. system
import importlib
import importlib.util
import json
import logging
import os
import sys
from collections import OrderedDict
# 2. 3rd party
# 3. django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
# 4. my
import converter
import utils
from consts import *
import forms


moduledict = dict()
logger = logging.getLogger(__name__)
PAGE_SIZE = 20


def eprint(s: str):
    print(s, file=sys.stderr)


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


def __load_modules(path):
    """
    Load all Python modules from a directory into a dict.

    :param path: the full path to the living place of the modules to load.
    :type path: :class:`str`
    :returns: map between loaded modules name and their content.
    :rtype: :class:`dict`
    """
    dir_list = os.listdir(path)
    mods = {}
    for fname in dir_list:
        name, ext = os.path.splitext(fname)
        if ext == '.py' and not name == '__init__':
            try:
                mods[name] = importlib.import_module('tpl.'+name)  # hack
            except Exception as ex:
                print("Unable load module '{}': {}".format(name, ex))
    return mods


def __try_tpl():
    global moduledict  # , modulelist
    if not moduledict:
        # 1. load modules into list of modulename=>module
        tpl = __load_modules(os.path.join(os.path.dirname(__file__), 'tpl'))  # {'z0000': <module>}
        # 2. repack
        for k, module in tpl.items():  # k: filename, v: module object
            # try: dict, getattr/setattr/hasattr/delattr, hash/hex/id
            # s = set(dir(module))
            data = module.DATA
            uuid = data[K_T_UUID]
            __tryget = module.__dict__.get
            # 2. dict
            moduledict[uuid] = {K_V_MODULE: module, }
            # 3. add dates fields
            datefields = list()
            for i, j in data[K_T_FIELD].items():  # each field definition:
                if j[K_T_FIELD_T] == K_DATE_FIELD:
                    datefields.append(i)
            if datefields:
                moduledict[uuid][K_V_DATES] = set(datefields)
            # 4. form
            if K_T_FORM in module.__dict__:  # create DynaForm
                form = module[K_T_FORM]
            else:
                form = forms.GenForm(fieldlist=data[K_T_FIELD])
            moduledict[uuid][K_T_FORM] = form
            # 5. formsets
            if K_T_FORMSETS in module.__dict__:  # create DynaForm
                formsets = module[K_T_FORMSETS]
            else:
                if K_T_S in data:
                    formsets = forms.GenFormSets(formlist=data[K_T_S])
                else:
                    formsets = OrderedDict()
            moduledict[uuid][K_T_FORMSETS] = formsets
        # eprint(moduledict)


def __try_to_call(t, f, v):
    """
    Try to call function f of module t[] with value v
    """
    if f in t[K_V_MODULE].__dict__:
        return t[K_V_MODULE].__dict__[f](v)


def try_tpl(fn):
    def _wrapped(*args, **kwargs):
        __try_tpl()
        return fn(*args, **kwargs)
    return _wrapped

# ====


class TplList(TemplateView):
    template_name = "tpl_list.html"

    @try_tpl
    def get_context_data(self, **kwargs):
        # __log_request(request)
        context = super().get_context_data(**kwargs)
        context['data'] = moduledict
        return context


def __doc_print(request, context_dict, template):
    ext = template.rsplit('.', 1)[1]
    return converter.x2pdf[ext](request, context_dict, template)


@try_tpl
def doc_a(request, uuid, mode=0):
    """
    Anon/Create/Update
    :param uuid:str - uuid (anon/create) or doc id (update)
    :param mode:int (0: anon (print), 1: create, 2: update)
    :return request, html_tpl_name, context:dict
    """
    __log_request(request)
    tpl = moduledict[uuid]
    # 1. check <pkg>.ANON/CREATE/UPDATE
    self_func = [K_T_F_ANON, K_T_F_ADD, K_T_F_EDIT][mode]
    if self_func in tpl[K_V_MODULE].__dict__:
        return tpl[K_V_MODULE].__dict__[self_func](request, pk)
    # else:
    # 2. get FORM and FORMSETS
    formclass = tpl[K_T_FORM]
    formsetsclass = tpl[K_T_FORMSETS]  # OrderedDict of dicts
    if request.method == 'POST':
        # pprint.pprint(request.POST['_action'])
        form = formclass(request.POST)
        # if mode == 0:  # ANON, Create/Update -> view/print
        del form.fields[K_T_F_NAME]
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
            __try_to_call(tpl, K_T_F_POST_FORM, data)
            # split
            # if mode == 0:  # ANON > PRINT, C/U -> V/P
            if (K_T_T in tpl[K_V_MODULE].DATA) and (K_T_T_PRINT in tpl[K_V_MODULE].DATA[K_T_T]):
                context_dict = {'data': data}
                template = tpl[K_V_MODULE].DATA[K_T_T][K_T_T_PRINT]
                if request.POST.get('_action', None) == u'view':
                    __try_to_call(tpl, K_T_F_PRE_VIEW, data)  # Create/Update -> View
                    return converter.html2html(request, context_dict, template)
                else:  # Anon/Create/Update -> PRINT
                    __try_to_call(tpl, K_T_F_PRE_PRINT, data)
                    return __doc_print(request, context_dict, template)
            else:  # tmp dummy
                return redirect('tpl_list')
    else:  # GET
        form = formclass()
        del form.fields[K_T_F_NAME]
        formlist = OrderedDict()
        for k, formset in formsetsclass.items():
            formlist[k] = formset(prefix=k)
    return render(request,
                  tpl[K_V_MODULE].DATA[K_T_T][K_T_T_FORM] if ((K_T_T in tpl[K_V_MODULE].DATA) and (
                          K_T_T_FORM in tpl[K_V_MODULE].DATA[K_T_T])) else 'auto_form.html',
                  context={
                      'name': tpl[K_V_MODULE].DATA[K_T_NAME],
                      'comments': tpl[K_V_MODULE].DATA.get(K_T_COMMENTS, ''),
                      'legend': tpl[K_V_MODULE].DATA.get(K_T_LEGEND, ''),
                      'uuid': tpl[K_V_MODULE].DATA[K_T_UUID],
                      'form': form,
                      'formlist': formlist,
                      'example': tpl[K_V_MODULE].DATA.get('example', None),
                  })
