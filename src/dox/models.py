# -*- coding: utf-8 -*-

# 1. system
# 3. django
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Doc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')  # editable-False
    updated = models.DateTimeField(auto_now=True, verbose_name=u'Изменен')  # editable-False
    type = models.CharField(max_length=32, verbose_name=u'Тип')
    name = models.CharField(max_length=32, verbose_name=u'Наименование')
    data = models.TextField(verbose_name=u'Данные')

    def __unicode__(self):
        return self.name

    # def save(self):
    #   if not self.id:
    #       self.created = datetime.date.today()
    #   self.updated = datetime.datetime.today()
    #   super(Doc, self).save()

    def get_absolute_url(self):
        return 'dox.views.doc_r', [str(self.id)]

    def get_edit_url(self):
        return reverse('dox.views.doc_u', args=[self.pk])

    def get_del_url(self):
        return reverse('dox.views.doc_d', args=[self.pk])

    class Meta:
        unique_together = (('user', 'type', 'name'),)
        ordering = ('type', 'name',)
        verbose_name = u'Документ'
        verbose_name_plural = u'Документы'


try:
    from local_models import *
except ImportError:
    pass
