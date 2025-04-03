from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tenant(User):
    id_image = models.ImageField(upload_to='properties_images/', blank=True, null=True)
    