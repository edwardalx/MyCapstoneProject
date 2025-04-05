from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group,Permission
from django.conf import settings

# Create your models here.
class Tenant(User):
    id_image = models.ImageField(upload_to='tenant_images/', blank=True, null=True)
    def __str__(self):
        return f"Name: {self.first_name}  Mobile:{self.phoneNumber} "

# class CustomUser(AbstractUser):  # ✅ Your custom user model
#     pass

# class Tenant(CustomUser):  # ✅ Tenant links to CustomUser
#     id_image = models.ImageField(upload_to='properties_images/', blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)  # Optional address field