

# Create your views here.

from django.shortcuts import render
from .models import Tenancy_Agreement
from .serializers import TenancySerialzer
from rest_framework import viewsets
from rest_framework import permissions

class TenancyApiViewset(viewsets.ModelViewSet):
    permission_classes = permissions.IsAuthenticated
    model = Tenancy_Agreement
    queryset = Tenancy_Agreement.objects.all()
    serializer_class = TenancySerialzer
