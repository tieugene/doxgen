# -*- coding: utf-8 -*-
'''
DoxGen Constants.
Naming:
 * K_ - key for dict:
  * K_T_ - key of template
'''

# Template keys
K_T_DATA	= 'DATA'
K_T_UUID	= 'u'		# inside K_T_DATA
K_T_NAME	= 'n'		# inside K_T_DATA
K_T_COMMENTS	= 'c'		# inside K_T_DATA
K_T_LEGEND	= 'legend'	# inside K_T_DATA
K_T_FIELD	= 'f'		# inside K_T_DATA - fields (main form)
K_T_FIELD_T	= 't'		# inside K_T_FIELD; hardcoded in auto_form
K_BOOL_FIELD	= 'b'		# value of K_T_FIELD_T
K_CHAR_FIELD	= 'c'
K_DATE_FIELD	= 'd'
K_INT_FIELD	= 'i'
K_DEC_FIELD	= '#'
K_CHOICE_FIELD	= 's'
K_MODEL_FIELD	= 'm'
K_INN_FIELD	= 'inn'
K_OGRN_FIELD	= 'ogrn'
K_T_FIELD_A	= 'a'		# inside K_T_FIELD; hardcoded in auto_view, auto_form, printforms
K_T_F_NAME	= 'name'	# extra field
K_T_S		= 's'		# inside K_T_DATA - fieldsets
K_T_T		= 't'		# inside K_T_DATA - templates
K_T_T_LIST	= 'l'		# inside K_T_T
K_T_T_FORM	= 'f'		# inside K_T_T
K_T_T_READ	= 'r'		# inside K_T_T
K_T_T_VIEW	= 'v'		# inside K_T_T
K_T_T_PRINT	= 'p'		# inside K_T_T
# forms and formsets
K_T_FORM	= 'FORM'	# in modulelidct too
K_T_FORMSETS	= 'FORMSETS'	# in modulelidct too
# triggers
K_T_F_LIST	= 'LIST'
K_T_F_ANON	= 'ANON'
K_T_F_ADD	= 'CREATE'
K_T_F_EDIT	= 'UPDATE'
K_T_F_READ	= 'READ'
K_T_F_VIEW	= 'VIEW'
K_T_F_PRINT	= 'PRINT'
#K_T_F_DEL	= 'DELETE'
K_T_F_PRE_FORM	= 'PRE_FORM'
K_T_F_PRE_SAVE	= 'PRE_SAVE'
K_T_F_PRE_READ	= 'PRE_READ'
K_T_F_PRE_VIEW	= 'PRE_VIEW'
K_T_F_PRE_PRINT	= 'PRE_PRINT'
K_T_F_POST_LOAD	= 'POST_LOAD'
K_T_F_POST_FORM	= 'POST_FORM'

# main views.py moduledict keys
# These keys are dynamically loaded - so, you can put here what you want. BUT - keep them uniq!
K_V_MODULE	= 'm'		# v
K_V_DATES	= 'dates'	# v	# set of date fields
