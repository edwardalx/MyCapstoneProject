
# Create your views here.
from django.shortcuts import render
from .models import Property,Unit,Image
from .serializers import PropertySerialzer,UnitSerialzer,ImageSerialzer
from rest_framework import viewsets

class PaymentApiViewset(viewsets.ModelViewSet):
    model = Property
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer


class UnitApiViewset(viewsets.ModelViewSet):
    model = Unit
    queryset = Unit.objects.all()
    serializer_class = UnitSerialzer

class ImageApiViewset(viewsets.ModelViewSet):
    model = Image
    queryset = Image.objects.all()
    serializer_class = PropertySerialzer

