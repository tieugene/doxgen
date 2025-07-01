"""Autostart
FIXME: calling twice
"""
import logging

from django.apps import AppConfig
from django.conf import settings
import forms
import core.converter
import core.mgr

class DoxGenConfig(AppConfig):
    name = 'doxgen'
    def ready(self):
        logging.info("Autostart:")
        logging.info("Loading engines...")
        core.converter.autostart()  # engines
        logging.info("Loading plugins...")  # plugins
        core.mgr.autostart(settings.PLUGINS_DIR, forms.generate_form, forms.generate_formset)
        logging.info("/Autostart")
