from __future__ import unicode_literals, absolute_import

from django.apps import AppConfig

class UsersAppConfig(AppConfig):

    name = "kamiair.apps.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
