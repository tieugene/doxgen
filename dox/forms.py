# -*- coding: utf-8 -*-
'''
http://snipt.net/danfreak/how-to-generate-a-dynamic-at-runtime-form-in-django/
'''

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe

import pprint

from consts import *

def	chk_inn(s):
	'''
	Check INN
	@param s:str - INN (e.g. 1234567894 or 123456789093)
	@return int - errcode:
		0 - ok
		1 - non-digits
		2 - wrong len
		3 - wrong check code
	'''
	k10 = (2, 4, 10, 3, 5, 9, 4, 6, 8)
	k11 = (7, 2, 4, 10, 3, 5, 9, 4, 9, 8)
	k12 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
	def chk_cs(s, k):
		'''
		Calculates cs
		@param s:str - inn
		@param k:tuple - koefficients
		@return boolean - CS ok
		'''
		sum = 0
		l = len(k)
		for i in xrange(l):
			sum += int(s[i]) * k[i]
		#print ((sum%11)%10)%11
		return ((sum%11)%10)%11 == int(s[l])
	if not s.isdigit():
		return 1
	if (len(s) == 10):
		return 0 if chk_cs(s, k10) else 3
	elif (len(s) == 12):
		return 0 if (chk_cs(s, k11) and chk_cs(s, k12)) else 3
	return 2

def	chk_ogrn(s):
	'''
	Check OGRN
	@param s:str - OGRN (e.g. 5067847579135)
	@return int - errcode:
		0 - ok
		1 - non-digits
		2 - wrong len
		3 - wrong check code
	'''
	if not s.isdigit():
		return 1
	if (len(s) != 13):
		return 2
	if (int(s[:12])%11)%10 != int(s[12]):
		return 3
	return 0


class	INNField(forms.CharField):
	def	clean(self, value):
		if (self.required):
			result = chk_inn(value)
			if (result == 1):
				raise forms.ValidationError(u'содержит не-цифры')
			elif (result == 2):
				raise forms.ValidationError(u'неверная длинна (должно быть 10 или 12)')
			elif (result == 3):
				raise forms.ValidationError(u'контрольное число не совпадает с вычисленным')
		return super(INNField, self).clean(value)

class	OGRNField(forms.CharField):
	def	clean(self, value):
		if (self.required):
			result = chk_ogrn(value)
			if (result == 1):
				raise forms.ValidationError(u'содержит не-цифры')
			elif (result == 2):
				raise forms.ValidationError(u'неверная длинна (должно быть 13)')
			elif (result == 3):
				raise forms.ValidationError(u'контрольные числа не совпадает с вычисленными')
		return super(OGRNField, self).clean(value)

field_dict = {
	K_BOOL_FIELD:	forms.BooleanField,
	K_CHAR_FIELD:	forms.CharField,
	K_DATE_FIELD:	forms.DateField,
	K_INT_FIELD:	forms.IntegerField,
	K_DEC_FIELD:	forms.DecimalField,
	K_CHOICE_FIELD:	forms.ChoiceField,
	K_MODEL_FIELD:	forms.ModelChoiceField,
	K_INN_FIELD:	INNField,
	K_OGRN_FIELD:	OGRNField,
}

def	GenForm(fieldlist, named=True):	# FIXME: form name (for formset class name)
	'''
	Generates Form class
	:param fieldlist:SortedDict - fields definitions
	Return form class
	'''
	#class	WrappedFormField():
	#	def as_divs(self):
	#		#pprint.pprint(self.__dict__)
	#		#return mark_safe(u'<div> <p> %s </p> <p> %s </p> <div>' % (self.label, self.widget.render('name', self.initial, self.widget_attrs(self.widget))))
	#		return mark_safe(u'<div> <p> %s </p> <p> %s </p> <div>' % (self.label, self))
	fields = SortedDict()
	if (named):
		#class t(forms.CharField, WrappedFormField):
		#	pass
		#fields[K_T_F_NAME] = t(label='Наименование', help_text='уникальное для данного типа документов')
		#fields[K_T_F_NAME] = forms.CharField(label='Наименование', help_text='уникальное для данного типа документов')
		fields[K_T_F_NAME] = forms.CharField(label='Наименование')
	for k, v in fieldlist.iteritems():
		#class t(field_dict[v[K_T_FIELD_T]], WrappedFormField):
		#	pass
		#fields[k] = t(**v[K_T_FIELD_A])
		fields[k] = field_dict[v[K_T_FIELD_T]](**v[K_T_FIELD_A])
	retvalue = type('DynaForm', (forms.BaseForm,), { 'base_fields': fields })
	retvalue.required_css_class = 'required'
	retvalue.error_css_class = 'error'
	return retvalue

# formset = formset_factory(OkvedForm)(request.POST)
# or
# MyFormSet = formset_factory(OkvedForm); formset = MyFormSet()
# So - class formset_factory(class)

def	GenFormSets(formlist):
	'''
	Generates SortedDict of Form sets classes
	:param fieldlist:SortedDict - fields sets definitions
	:return SortedDict { k: formset class }
	'''
	retvalue = SortedDict()
	for k, v in formlist.iteritems():	# i:str - formset key, j:{ K_T_FIELD_A: {}, K_T_FIELD_T: SortedDict() } - of fields definitions
		retvalue[k] = formset_factory(GenForm(v[K_T_FIELD_T], named = False))
	return retvalue

try:
        from local_forms import *
except ImportError:
        pass
