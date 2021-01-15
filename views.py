# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.conf import settings


def index(request):
    return redirect('dox.views.index')


def common_context(context):
    """
    our context processor. Add to dict vars to send in ALL templates.
    """
    return {
        'LOGIN_URL': settings.LOGIN_URL,
        'path': 'apps.core'
    }
