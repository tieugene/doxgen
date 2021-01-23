# -*- coding: utf-8 -*-
"""
http://snipt.net/danfreak/how-to-generate-a-dynamic-at-runtime-form-in-django/
"""

from collections import OrderedDict

from django import forms
from django.forms.formsets import formset_factory

from core.consts import *
from misc.utils import chk_inn, chk_ogrn


class INNField(forms.CharField):
    def clean(self, value):
        if self.required:
            result = chk_inn(value)
            if result == 1:
                raise forms.ValidationError(u'содержит не-цифры')
            elif result == 2:
                raise forms.ValidationError(u'неверная длинна (должно быть 10 или 12)')
            elif result == 3:
                raise forms.ValidationError(u'контрольное число не совпадает с вычисленным')
        return super(INNField, self).clean(value)


class OGRNField(forms.CharField):
    def clean(self, value):
        if self.required:
            result = chk_ogrn(value)
            if result == 1:
                raise forms.ValidationError(u'содержит не-цифры')
            elif result == 2:
                raise forms.ValidationError(u'неверная длинна (должно быть 13)')
            elif result == 3:
                raise forms.ValidationError(u'контрольные числа не совпадает с вычисленными')
        return super(OGRNField, self).clean(value)


field_dict = {
    K_BOOL_FIELD: forms.BooleanField,
    K_CHAR_FIELD: forms.CharField,
    K_DATE_FIELD: forms.DateField,
    K_INT_FIELD: forms.IntegerField,
    K_DEC_FIELD: forms.DecimalField,
    K_CHOICE_FIELD: forms.ChoiceField,
    K_MODEL_FIELD: forms.ModelChoiceField,
    K_INN_FIELD: INNField,
    K_OGRN_FIELD: OGRNField,
}


def GenForm(fieldlist, named=True):  # FIXME: form name (for formset class name)
    """
    Generates Form class
    :param fieldlist:OrderedDict - fields definitions
    :param named:
    Return form class
    """
    fields = OrderedDict()
    if named:
        fields[K_T_F_NAME] = forms.CharField(label='Наименование')
    for k, v in fieldlist.items():
        fields[k] = field_dict[v[K_T_FIELD_T]](**v[K_T_FIELD_A])
    retvalue = type('DynaForm', (forms.BaseForm,), {'base_fields': fields})
    retvalue.required_css_class = 'required'
    retvalue.error_css_class = 'error'
    return retvalue


def GenFormSets(formlist):
    """
    Generates OrderedDict of Form sets classes
    :param formlist: ???
    :param fieldlist:OrderedDict - fields sets definitions
    :return OrderedDict { k: formset class }
    """
    retvalue = OrderedDict()
    for k, v in formlist.items():  # i:str - formset key, j:{ K_T_FIELD_A: {}, K_T_FIELD_T: OrderedDict() } - of fields definitions
        retvalue[k] = formset_factory(GenForm(v[K_T_FIELD_T], named=False))
    return retvalue


try:
    from local_forms import *
except ImportError:
    pass
