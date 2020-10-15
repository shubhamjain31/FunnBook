from django.apps import AppConfig


class UserpageConfig(AppConfig):
    name = 'UserPage'

    def ready(self):
    	import UserPage.signals
