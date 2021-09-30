from django.apps import AppConfig


class InterstoreAppConfig(AppConfig):
    """ присвоение verbose_name приложению mainapp в административной панели"""

    name = "mainapp"
    verbose_name = "Главное приложение"
