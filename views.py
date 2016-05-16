# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.conf import settings

def	index(request):
	return redirect('dox.views.index')
	#return direct_to_template(request, 'index.html')

def	about(request):
	return direct_to_template(request, 'about.html')

def	service(request):
	return direct_to_template(request, 'service.html')

def	common_context(context):
	'''
	our context processor. Add to dict vars to send in ALL templates.
	'''
	return {
		'LOGIN_URL' : settings.LOGIN_URL,
		'path': 'apps.core'
	}
