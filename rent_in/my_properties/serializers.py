from rest_framework import serializers
from .models import Property, Unit, Image
class PropertySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

# class UnitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Unit
#         fields = '__all__'
# 

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['property', 'room_number', 'cost', 'max_no_of_people']

class ImageSerialzer(serializers.ModelSerializer):
    property = PropertySerialzer( read_only = True)
    unit = UnitSerializer( read_only = True)

    class Meta:
        model = Image
        fields = '__all__'