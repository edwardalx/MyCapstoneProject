

# Create your views here.

from django.shortcuts import render
from .models import Tenancy_Agreement
from .serializers import TenancySerialzer
from rest_framework import viewsets

class TenancyApiViewset(viewsets.ModelViewSet):
    model = Tenancy_Agreement
    queryset = Tenancy_Agreement.objects.all()
    serializer_class = TenancySerialzer