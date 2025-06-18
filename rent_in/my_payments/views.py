from datetime import timezone
import requests
import uuid
import hashlib
import hmac
from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment, PaymentSummary
from accounts.models import Tenant
from my_tenancy.models import Tenancy_Agreement
from my_properties.models import Property, Unit
from .serializers import PaymentSummarySerialzer, PaymentSerialzer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework import permissions,authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.decorators import jwt_required


import logging
from django.conf import settings
logger = logging.getLogger(__name__)
# Create your views here.
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY  # Replace with your actual key
@jwt_required
def payment_page(request):
    unit_id = request.GET.get("unit_id")
    unit = None
    property = None
    reference = None

    # Try to get the unit if passed in querystring
    if unit_id:
        try:
            unit = Unit.objects.select_related('property').get(id=unit_id)
            property = unit.property
        except Unit.DoesNotExist:
            pass

    # Get the tenant's tenancy agreement if it exists
    try:
        agreement = Tenancy_Agreement.objects.get(tenant=request.user)
    except Tenancy_Agreement.DoesNotExist:
        agreement = None

    return render(request, "my_payments/newPaymentFlow.html", {
        "user": request.user,
        "tenancy_agreement": agreement,
        "unit": unit,
        "property": property,
        "reference":reference,
        "properties": Property.objects.all(),  # Needed for the property <select>
    })

@login_required
def payment_history(request):
    tenant = request.user  # assuming `user` is linked to a `Tenant` via OneToOne
    history = PaymentSummary.objects.filter(tenant=tenant).order_by('-last_payment_date')
    return render(request, 'my_payments/history.html', {'history': history})

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

    expected_signature = hmac.new(secret, body, hashlib.sha512).hexdigest()
    if not signature or not hmac.compare_digest(signature, expected_signature):
        return JsonResponse({"error": "Invalid signature"}, status=403)

    payload = json.loads(body)
    if payload['event'] == 'charge.success':
        data = payload['data']
        reference = data['reference']
        amount = int(data['amount']) // 100
        metadata = data.get('metadata', {})

        try:
            payment = Payment.objects.get(reference=reference)

            if payment.status == 'success':
                return HttpResponse(status=200)  # Already handled

            payment.status = 'success'
            payment.amount = amount
            payment.save()

            tenant = Tenant.objects.get(id=metadata['tenant_id'])
            unit = Unit.objects.get(id=metadata['unit_id'])

            tenancy_agreement, _ = Tenancy_Agreement.objects.get_or_create(
                tenant=tenant,
                unit=unit,
                defaults={
                    'contract_start_date': timezone.now().date(),
                    'contract_duration': 12  # or from metadata
                }
            )
            tenancy_agreement.total_amount_paid = (tenancy_agreement.total_amount_paid or 0) + amount
            tenancy_agreement.save()

            summary, _ = PaymentSummary.objects.get_or_create(tenancy_agreement=tenancy_agreement)
            summary.total_amount_paid = (summary.total_amount_paid or 0) + amount
            summary.amount_left = unit.cost - summary.total_amount_paid
            summary.last_payment_date = timezone.now().date()
            summary.save()

            unit.availability = False
            unit.save()

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
        except Tenant.DoesNotExist:
            return JsonResponse({"error": "Tenant not found"}, status=404)
        except Unit.DoesNotExist:
            return JsonResponse({"error": "Unit not found"}, status=404)

    return HttpResponse(status=200)

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from .models import Payment, Unit
import uuid, requests

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def initialize_payment(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    amount = request.data.get('amount')  # Should be in pesewas (e.g. 20000 for GHS 200)
    provider = request.data.get('provider')
    unit_id = request.data.get('unit_id')

    tenant = request.user  # Logged-in tenant

    # Validate inputs
    if not all([email, phone, amount, provider, unit_id]):
        return Response({"error": "Missing required fields"}, status=400)

    try:
        unit = Unit.objects.get(id=unit_id)
    except Unit.DoesNotExist:
        return Response({"error": "Unit does not exist"}, status=404)

    # Generate unique reference
    reference = str(uuid.uuid4())
    callback_url = f"http://127.0.0.1:8000/payments/receipt/{reference}/"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": email,
        "amount": int(amount),
        "currency": "GHS",
        "reference": reference,
        "metadata": {
            "phone": phone,
            "tenant_id": tenant.id,
            "unit_id": unit.id,
            "provider": provider
        },
        "callback_url": callback_url
    }

    try:
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers=headers,
            json=payload
        )
        res_data = response.json()

        if res_data.get('status'):
            # ✅ Create the Payment record BEFORE redirect
            Payment.objects.create(
                tenant=tenant,
                unit=unit,
                amount=int(amount) / 100,  # Store in GHS
                phone=phone,
                provider=provider,
                reference=reference,
                status='pending'
            )

            return Response({
                "status": True,
                "message": "Payment initiated",
                "data": res_data['data']
            })
        else:
            return Response({
                "status": False,
                "error": res_data.get('message', 'Paystack error')
            }, status=400)

    except requests.RequestException as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def verify_payment(request, reference):
    # 1. Verify with Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return Response({"detail": "Paystack verification failed"}, status=response.status_code)

    data = response.json()["data"]
    if data["status"] != "success":
        return Response({"detail": "Transaction not successful"}, status=400)

    # 2. Update payment
    payment = get_object_or_404(Payment, reference=reference)
    if payment.status != "completed":
        payment.status = "completed"
        payment.save()

        # 3. Mark unit as unavailable
        unit = payment.unit
        unit.availability = False
        unit.save()

    return Response({
        "status": "success",
        "message": "Payment successfully verified.",
        "reference": payment.reference,
        "amount": payment.amount, 
    })

def payment_receipt(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    context = {
        "reference": reference,
        "amount": payment.amount,
        "status": payment.status
    }
    return render(request, "my_payments/receipt.html", context)

