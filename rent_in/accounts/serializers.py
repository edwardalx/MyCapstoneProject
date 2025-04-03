from rest_framework import serializers
from .models import Tenant
from django.contrib .auth import get_user_model

User = get_user_model()
class TenantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Hide password from responses
    class Meta:
        model = Tenant
        feilds = '__all__','password'
    def get_full_name(self, obj):
        fullname = obj.first_name + " "+ obj.last_name
        return fullname
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  
        return user