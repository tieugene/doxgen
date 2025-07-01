import logging

from django.apps import AppConfig
import core.converter

class DoxGenConfig(AppConfig):
    name = 'doxgen'
    def ready(self):
        logging.info("Autostart:")
        # refs
        core.converter.autostart()  # engines
        # plugins
        logging.info("/Autostart")
