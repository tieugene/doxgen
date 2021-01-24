# -*- coding: utf-8 -*-
"""
core.mgr - plugins managenebt
"""

import os
import sys
import importlib
from collections import OrderedDict
from .consts import *

moduledict = dict()


def try_to_call(t, f, v):
    """
    Try to call function f of module t[] with value v
    """
    if f in t[K_V_MODULE].__dict__:
        return t[K_V_MODULE].__dict__[f](v)


def __load_modules(path: str) -> list:
    """
    Load all Python modules from a directory into a dict.

    :param path: the full path to the living place of the modules to load.
    :type path: :class:`str`
    :returns: map between loaded modules name and their content.
    :rtype: :class:`dict`
    """
    mods = list()   # modulename: module
    for dir_name in os.listdir(path):
        dir_path = os.path.join(path, dir_name)
        if os.path.isdir(dir_path):
            file_path = os.path.join(dir_path, 'main.py')
            if os.path.isfile(file_path):
                try:
                    mods.append(importlib.import_module('plugins.{}.main'.format(dir_name)))
                except Exception as ex:
                    print("Unable load module from plugins/'{}': {}".format(dir_name, ex), file=sys.stderr)
    return mods


def try_load_plugins(plugins_path: str, formgen, formsetgen) -> None:
    """
    Fill moduledict if it is not loaded
    :param plugins_path: path where plugins are
    :param formgen: main form generator (callback)
    :param formsetgen: formset (multiline part) generator (callback)
    :return: None
    """
    if not moduledict:
        # 1. load modules into list of modulename=>module
        # 2. repack
        for module in __load_modules(plugins_path):  # repack module objects
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
                form = formgen(fieldlist=data[K_T_FIELD])
            moduledict[uuid][K_T_FORM] = form
            # 5. formsets
            if K_T_FORMSETS in module.__dict__:  # create DynaForm
                formsets = module[K_T_FORMSETS]
            else:
                if K_T_S in data:
                    formsets = formsetgen(formlist=data[K_T_S])
                else:
                    formsets = OrderedDict()
            moduledict[uuid][K_T_FORMSETS] = formsets
