# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models

class	DocAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'user', 'type', 'name', 'created', 'updated')

class	LogAdmin(admin.ModelAdmin):
	ordering	= ('id',)
	list_display	= ('id', 'date', 'method', 'ip', 'path', 'agent')

admin.site.register(models.Doc,	DocAdmin)
admin.site.register(models.Log,	LogAdmin)

try:
        from local_admin import *
except ImportError:
        pass
