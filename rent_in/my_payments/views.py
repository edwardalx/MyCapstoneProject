from django.shortcuts import render
from .models import Payment
from .serializers import PaymentSerialzer
from rest_framework import viewsets
# Create your views here.
class PaymentApiViewset(viewsets.ModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerialzer

