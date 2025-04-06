from rest_framework import serializers
from .models import Tenant
from django.contrib .auth import get_user_model

User = get_user_model()
class TenantSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^\d+$',error_messages={"invalid": "Username must contain only numbers."}
    )
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)  # Hide password from responses
    class Meta:
        model = Tenant
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def get_full_name(self, obj):
        fullname = f"{obj.first_name}  {obj.last_name}"
        return fullname
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  
        return user