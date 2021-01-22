# -*- coding: utf-8 -*-
"""
dox.urls
"""

from django.urls import path, register_converter

from . import converters, views

register_converter(converters.ShortUUIDConverter, 'tuid')

urlpatterns = [
	path('',					views.TplList.as_view(), name='tpl_list'),		# +
	path('l/',					views.LogList.as_view(), name='log_list'),		# -
	path('l/<int:pk>/',			views.LogDetail.as_view(), name='log_view'),	# -
	path('d/<tuid:uuid>/',		views.DocList.as_view(), name='doc_list'),		# - list (GET)
	# acu
	path('d/<tuid:uuid>/a/',	views.doc_a, name='doc_anon'),					# + anon (GET/POST=>print))	TODO: POST>view
	path('d/<tuid:uuid>/c/',	views.doc_c, name='doc_add'),					# + create (GET/POST=>save)	TODO: POST=>print/view
	path('d/<int:pk>/u/',		views.doc_u, name='doc_upd'),					# - update (GET/POST=>save)	TODO: POST=>print/view
	# rvp
	path('d/<int:pk>/r/',		views.doc_r, name='doc_read'),					# - read (GET)
	path('d/<int:pk>/v/',		views.doc_v, name='doc_view'),					# + [pre]view (GET)
	path('d/<int:pk>/p/',		views.doc_p, name='doc_prn'),					# + print (GET)
	#
	path('d/<int:pk>/d/',		views.doc_d, name='doc_del'),					# - delete (GET)
]
