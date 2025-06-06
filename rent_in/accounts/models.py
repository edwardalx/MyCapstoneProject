from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group,Permission
from django.conf import settings
import re
from django.core.exceptions import ValidationError

# Create your models here.
class Tenant(AbstractUser):   
    id_image = models.ImageField(upload_to='tenant_images/', blank=True, null=True)
    age = models.IntegerField(blank=True,null=True )
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    groups = models.ManyToManyField(Group, related_name="customer_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customer_permissions", blank=True)
    def __str__(self):
        return f"Name: {self.get_full_name()}  Mobile:{self.username} "

class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    def __str__(self):
        return f"Name: {self.user.first_name}  Mobile:{self.user.username} "

# class CustomUser(AbstractUser):  # ✅ Your custom user model
#     pass

# class Tenant(CustomUser):  # ✅ Tenant links to CustomUser
#     id_image = models.ImageField(upload_to='properties_images/', blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)  # Optional address field