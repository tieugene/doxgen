# -*- coding: utf-8 -*-

# 1. django
from django.db import models
from django.contrib.auth.models import User

# 3. system
import datetime, json

'''
class	UserExt:
	pass
'''

class   Doc(models.Model):
	user		= models.ForeignKey(User, verbose_name=u'Пользователь')
	created		= models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')	# editable-False
	updated		= models.DateTimeField(auto_now=True, verbose_name=u'Изменен')		# editable-False
	type		= models.CharField(max_length=32, verbose_name=u'Тип')
	name		= models.CharField(max_length=32, verbose_name=u'Наименование')
	data		= models.TextField(verbose_name=u'Данные')

	def     __unicode__(self):
		return self.name

	#def save(self):
	#	if not self.id:
	#		self.created = datetime.date.today()
	#	self.updated = datetime.datetime.today()
	#	super(Doc, self).save()

	@models.permalink
	def get_absolute_url(self):
		return ('dox.views.doc_r', [str(self.id)])

	def get_edit_url(self):
		return reverse('dox.views.doc_u', args=[self.pk])

	def get_del_url(self):
		return reverse('dox.views.doc_d', args=[self.pk])

	class   Meta:
		unique_together		= (('user', 'type', 'name'),)
		ordering                = ('type', 'name', )
		verbose_name            = u'Документ'
		verbose_name_plural     = u'Документы'

class   Log(models.Model):
	date		= models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
	method		= models.BooleanField(verbose_name=u'Метод')
	ip		= models.IPAddressField(verbose_name=u'IP')
	path		= models.CharField(max_length=255, verbose_name=u'Куда')
	agent		= models.CharField(null=True, max_length=255, verbose_name=u'Агент')
	data		= models.TextField(verbose_name=u'Данные')

	def	__unicode__(self):
		return self.ip

	class   Meta:
		ordering                = ('date',)
		verbose_name            = u'Лог'
		verbose_name_plural     = u'Логи'

try:
        from local_models import *
except ImportError:
        pass
