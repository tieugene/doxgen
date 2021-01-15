# -*- coding: utf-8 -*-
"""
dox.urls
"""

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('',								views.index),
	path('log/',							views.LogList.as_view()),
	re_path(r'^log/(?P<pk>\d+)/$',			views.LogDetail.as_view()),
	re_path(r'^(?P<uuid>[0-9A-Z]{32})/$',	views.doc_l),		# list (GET)
	# acu
	re_path(r'^(?P<uuid>[0-9A-Z]{32})/a/$',	views.doc_a),		# anon (GET/POST=>print))	TODO: POST>view
	re_path(r'^(?P<uuid>[0-9A-Z]{32})/c/$',	views.doc_c),		# create (GET/POST=>save)	TODO: POST=>print/view
	re_path(r'^(?P<pk>\d+)/u/$',			views.doc_u),		# update (GET/POST=>save)	TODO: POST=>print/view
	# rvp
	re_path(r'^(?P<pk>\d+)/r/$',			views.doc_r),		# read (GET)
	re_path(r'^(?P<pk>\d+)/v/$',			views.doc_v),		# [pre]view (GET)
	re_path(r'^(?P<pk>\d+)/p/$',			views.doc_p),		# print (GET)
	#
	re_path(r'^(?P<pk>\d+)/d/$',			views.doc_d),		# delete (GET)
]
