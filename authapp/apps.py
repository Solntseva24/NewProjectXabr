from django.apps import AppConfig


class InterstoreAppConfig(AppConfig):
    """ присвоение verbose_name приложению authapp в административной панели"""

    name = "authapp"
    verbose_name = "аутентификация"
