from django.apps import AppConfig
import os

class MainappConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import jobs

        # if os.environ.get('RUN_MAIN', None) != 'true':
        jobs.start_scheduler()

class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from . import jobs

        # if os.environ.get('RUN_MAIN', None) != 'true':
        jobs.start_scheduler()