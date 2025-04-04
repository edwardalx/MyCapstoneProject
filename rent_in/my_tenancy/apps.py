from django.apps import AppConfig


class MyTenancyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_tenancy'
