from datetime import timezone
import uuid
import hashlib
import hmac
from django.shortcuts import render
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment, PaymentSummary
from accounts.models import Tenant
from my_tenancy.models import Tenancy_Agreement
from .serializers import PaymentSummarySerialzer, PaymentSerialzer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required

# Create your views here.
PAYSTACK_SECRET_KEY = "sk_test_xxx"  # Replace with your actual key
@login_required
def payment_page(request):
    return render(request, 'payments/payments.html')

@login_required
def payment_history(request):
    tenant = request.user  # assuming `user` is linked to a `Tenant` via OneToOne
    history = PaymentSummary.objects.filter(tenant=tenant).order_by('-last_payment_date')
    return render(request, 'payments/history.html', {'history': history})

class PaymentSummaryApiViewset(viewsets.ModelViewSet):
    model = PaymentSummary
    queryset = PaymentSummary.objects.all()
    serializer_class = PaymentSummarySerialzer

class PaymentApiViewset(viewsets.ModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerialzer

@csrf_exempt
def paystack_webhook(request):
    secret = settings.PAYSTACK_SECRET_KEY.encode()
    signature = request.headers.get('X-Paystack-Signature')
    body = request.body

    # Verify Paystack signature
    if not signature or not hmac.compare_digest(signature, hmac.new(secret, body, hashlib.sha512).hexdigest()):
        return JsonResponse({"error": "Invalid signature"}, status=403)

    payload = json.loads(body)

    if payload['event'] == 'charge.success':
        data = payload['data']
        reference = data['reference']
        amount = int(data['amount']) // 100  # Convert from kobo to GHS
        email = data['customer']['email']
        phone = data.get('metadata', {}).get('phone')
        tenancy_id = data.get('metadata', {}).get('tenancy_agreement_id')

        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = 'success'
            payment.amount = amount
            payment.save()

            # Get related tenant and tenancy agreement
            tenant = Tenant.objects.get(email=email)
            tenancy_agreement = Tenancy_Agreement.objects.get(tenant=tenant)

            # Update or create PaymentSummary
            summary, created = PaymentSummary.objects.get_or_create(tenancy_agreement=tenancy_agreement)
            summary.total_amount_paid += amount
            summary.amount_left = tenancy_agreement.unit.cost - summary.total_amount_paid
            summary.last_payment_date = timezone.now().date()
            summary.save()

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
        except (Tenant.DoesNotExist, Tenancy_Agreement.DoesNotExist):
            return JsonResponse({"error": "Tenant or agreement not found"}, status=404)

    return HttpResponse(status=200)

@csrf_exempt
def initialize_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = str(uuid.uuid4())

        tenancy_agreement_id = data.get('tenancy_agreement_id')
        if not tenancy_agreement_id:
            return JsonResponse({"error": "Missing tenancy_agreement_id"}, status=400)

        headers = {
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            "email": data['email'],
            "amount": data['amount'],
            "currency": "GHS",
            "channels": ["mobile_money"],
            "mobile_money": {
                "phone": data['phone'],
                "provider": data['provider']
            },
            "reference": reference,
            "metadata": {
                "phone": data['phone'],
                "tenancy_agreement_id": tenancy_agreement_id
            }
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
        res_data = response.json()

        if res_data.get('status'):
            # Optionally, associate the Payment with the agreement or tenant if available
            Payment.objects.create(
                email=data['email'],
                amount=data['amount'],
                phone=data['phone'],
                provider=data['provider'],
                reference=reference,
                # You can later update it to add foreign keys like `tenant` or `property`
            )
            return JsonResponse(res_data)
        else:
            return JsonResponse({"error": "Payment initialization failed"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def verify_payment(request, reference):
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    res_data = response.json()

    if res_data.get('status') and res_data['data']['status'] == 'success':
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = "success"
            payment.save()
            return JsonResponse({"message": "Payment successful", "data": res_data['data']})
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

    return JsonResponse({"error": "Verification failed"}, status=400)
