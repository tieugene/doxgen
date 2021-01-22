from django.contrib import admin
# from django.conf.urls import url
from django.urls import include, path, register_converter
from django.views.generic.base import TemplateView

import misc.utils
import views

register_converter(misc.utils.ShortUUIDConverter, 'tuid')

urlpatterns = [
	path('user/',			include('django.contrib.auth.urls')),
	path('admin/',			admin.site.urls),
	path('about/',			TemplateView.as_view(template_name='about.html'), name='about'),
	path('', 				TemplateView.as_view(template_name='index.html'), name='index'),
	path('t/', 				views.TplList.as_view(), name='tpl_list'),
	path('d/<tuid:uuid>/',	views.doc_a, name='doc_anon'),  # + anon (GET/POST=>print))	TODO: POST>view
]
