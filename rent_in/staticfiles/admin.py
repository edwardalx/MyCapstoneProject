from django.contrib import admin
from .models import Tenant, Manager

# Register your models here.
admin.site.register([Tenant, Manager])