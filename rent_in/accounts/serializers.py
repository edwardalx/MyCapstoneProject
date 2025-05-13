from rest_framework import serializers
from .models import Tenant
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib .auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()
class TenantSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^\d+$',error_messages={"invalid": "Username must contain only numbers."}
    )
    password = serializers.CharField(write_only=True)  # Hide password from responses
    class Meta:
        model = Tenant
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # def get_full_name(self, obj):
    #     fullname = f"{obj.first_name}  {obj.last_name}"
    #     return fullname
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  
        return user
class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone = attrs.get("username")  # still using "username" from frontend
        password = attrs.get("password")

        try:
            user = User.objects.get(username=phone)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid phone number or password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid phone number or password")

        data = super().validate(attrs)
        data['username'] = user.username
        return data