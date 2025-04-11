from django.contrib import admin
from .models import Property,Unit,Image
# Register your models here.
admin.site.register([Property,Unit,Image])