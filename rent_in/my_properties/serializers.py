from rest_framework import serializers
from .models import Property, Unit, Image
class PropertySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class UnitSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class ImageSerialzer(serializers.ModelSerializer):
    property = PropertySerialzer( read_only = True)
    unit = UnitSerialzer( read_only = True)

    class Meta:
        model = Image
        fields = '__all__'