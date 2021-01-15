from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView, RedirectView

import views

urlpatterns = [
	path('',		TemplateView.as_view(template_name='index.html'), name='index'),
	path('about/',	TemplateView.as_view(template_name='about.html'), name='about'),
	path('admin/',	admin.site.urls),
	path('doxgen/',	include('dox.urls')),
	# path('login/',	'django.contrib.auth.views.login'),
	# path('logout/',	'django.contrib.auth.views.logout'),
	#path('admin/jsi18n',	'django.views.i18n.javascript_catalog'), # hack to use admin form widgets
	#(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
	# url(r'^$', 'doxgen.views.home', name='home'),
]
