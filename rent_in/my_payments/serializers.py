from rest_framework import serializers
from .models import PaymentSummary,Payment


class PaymentSummarySerialzer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSummary
        fields = '__all__'


class PaymentSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'