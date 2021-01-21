from django.contrib import admin
# from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView, RedirectView

urlpatterns = [
	path('user/',	include('django.contrib.auth.urls')),
	path('admin/',	admin.site.urls),
	path('',		TemplateView.as_view(template_name='index.html'), name='index'),
	path('about/',	TemplateView.as_view(template_name='about.html'), name='about'),
	path('dox/',	include('dox.urls')),
]
