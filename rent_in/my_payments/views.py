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
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

import logging
from django.conf import settings
logger = logging.getLogger(__name__)
# Create your views here.
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY  # Replace with your actual key
@login_required
def payment_page(request):
    unit_id = request.GET.get("unit_id")
    unit = None
    property = None

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
        tenant_id = data.get('metadata', {}).get('tenant_id')
        unit_id = data.get('metadata', {}).get('unit_id')

        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = 'success'
            payment.amount = amount
            payment.save()

            # Get related tenant and tenancy agreement
            tenant = Tenant.objects.get(tenant_id=tenant_id)
            unit = Unit.objects.get(unit_id=unit_id)
            # Update or create Tenancy_Agreement
            tenancy_agreement, created = Tenancy_Agreement.objects.get_or_create(tenant=tenant)
            tenancy_agreement.total_amount_paid += amount
            tenancy_agreement.save()
            # Update or create PaymentSummary
            summary, created = PaymentSummary.objects.get_or_create(tenancy_agreement=tenancy_agreement)
            summary.total_amount_paid += amount
            summary.amount_left = unit.cost - summary.total_amount_paid
            summary.last_payment_date = timezone.now().date()
            summary.save()
           

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
        except (Tenant.DoesNotExist, Tenancy_Agreement.DoesNotExist):
            return JsonResponse({"error": "Tenant or agreement not found"}, status=404)

    return HttpResponse(status=200)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initialize_payment(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    amount = request.data.get('amount')  # Should be in pesewas
    provider = request.data.get('provider')
    unit_id = request.data.get('unit_id')

    tenant_id = request.user.id  # ✅ Secure tenant_id from logged-in user

    if not all([email, phone, amount, provider, unit_id]):
        return Response({"error": "Missing required fields"}, status=400)

    reference = str(uuid.uuid4())
    callback_url= f"https://edwardalx.pythonanywhere.com/payments/verify/{reference}/"
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
            "tenant_id": tenant_id,
            "unit_id": unit_id,
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
@permission_classes([permissions.IsAuthenticated])
def verify_payment(request, reference):
    # This view will verify the payment status from Paystack (or another provider)
    # For simplicity, let's assume the payment is successful.
    payment = get_object_or_404(Payment, reference=reference)

    # Once payment is successful, update the status of the payment
    payment.status = "completed"
    payment.save()

      # Mark unit as unavailable
    unit = payment.unit
    unit.availability = False
    unit.save()
    # Return success message
    return Response({
        "status": "success",
        "message": "Payment successfully verified."
    })
