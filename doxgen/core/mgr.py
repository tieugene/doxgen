# -*- coding: utf-8 -*-
"""
core.mgr - plugins managenebt
"""
# 1. system
import pathlib
import importlib
import logging
from collections import OrderedDict
from .consts import *
from .converter import x2pdf
# 2. 3rd parties
# 3. django
# from django.utils.translation import gettext as _


plugins_dict = dict()


def try_to_call(t, f, v):
    """
    Try to call function f of module t[] with value v
    """
    if f in t[K_V_MODULE].__dict__:
        logging.info("try_to_call", type(t[K_V_MODULE].__dict__[f](v)))
        return t[K_V_MODULE].__dict__[f](v)

def __load_plugin(plugins_dir: pathlib.Path) -> list:
    """
    Load all Python plugin from a directory into a dict.

    :param plugins_dir: the full path to the living place of the plugins to load.
    :type plugins_dir: :class:`str`
    :returns: map between loaded modules name and their content.
    :rtype: :class:`dict`
    """
    mods = list()   # [(plugindir:str, module:str),]
    for dir_name in plugins_dir.iterdir():
        # logging.info("dir_name:", dir_name)
        dir_path = plugins_dir / dir_name
        if dir_path.is_dir():
            file_path = dir_path / 'main.py'
            if file_path.is_file():
                mod_name = f'plugins.{dir_name.name}.main'
                # logging.info("mod_name: %s", mod_name)
                try:
                    mods.append((str(dir_name), importlib.import_module(mod_name)))
                except ModuleNotFoundError as e:
                    logging.error("%s (%s): %s", __file__, mod_name, e)
    return mods


def try_load_plugins(plugins_path: pathlib.Path, formgen, formsetgen) -> None:
    """
    Fill moduledict if it is not loaded
    :param plugins_path: path where plugins are
    :param formgen: main form generator (callback)
    :param formsetgen: formset (multiline part) generator (callback)
    :return: None
    """
    if not plugins_dict:
        # 1. load modules into list of modulename=>module
        # 2. repack
        for dir_name, module in __load_plugin(plugins_path):  # repack module objects
            # s = set(dir(module))
            data = module.DATA
            if data[K_T_T] and data[K_T_T].get(K_T_T_ENGINE) not in x2pdf:
                logging.warning("Plugin '%s' skipped due not engine.", data[K_T_NAME])
                continue
            uuid = data[K_T_UUID]
            __tryget = module.__dict__.get
            # 2. dict
            plugins_dict[uuid] = {K_V_MODULE: module, K_T_DIR: dir_name}
            # 3. add dates fields
            datefields = list()
            for i, j in data[K_T_FIELD].items():  # each field definition:
                if j[K_T_FIELD_T] == K_DATE_FIELD:
                    datefields.append(i)
            if datefields:
                plugins_dict[uuid][K_V_DATES] = set(datefields)
            # 4. form
            if K_T_FORM in module.__dict__:  # create DynaForm
                form = module[K_T_FORM]
            else:
                form = formgen(fieldlist=data[K_T_FIELD])
            plugins_dict[uuid][K_T_FORM] = form
            # 5. formsets
            if K_T_FORMSETS in module.__dict__:  # create DynaForm
                formsets = module[K_T_FORMSETS]
            else:
                if K_T_S in data:
                    formsets = formsetgen(formlist=data[K_T_S])
                else:
                    formsets = OrderedDict()
            plugins_dict[uuid][K_T_FORMSETS] = formsets
