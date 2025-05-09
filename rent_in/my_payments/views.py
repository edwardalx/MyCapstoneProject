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
from my_properties.models import Unit
from .serializers import PaymentSummarySerialzer, PaymentSerialzer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
import logging
from django.conf import settings
logger = logging.getLogger(__name__)
# Create your views here.
PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY  # Replace with your actual key
@login_required
def payment_page(request):
    try:
        agreement = Tenancy_Agreement.objects.get(tenant=request.user)
    except Tenancy_Agreement.DoesNotExist:
        agreement = None  # or handle differently

    return render(request, "my_payments/payments.html", {
        "user": request.user,
        "tenancy_agreement": agreement
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

@csrf_exempt
def initialize_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received payment initialization request: {data}")

            tenant_id = data.get('tenant_id')
            if not tenant_id:
                logger.error("Missing tenant_id in request data")
                return JsonResponse({"error": "Missing tenant_id"}, status=400)

            try:
                tenant = Tenant.objects.get(id=tenant_id)
            except Tenancy_Agreement.DoesNotExist:
                logger.error(f"Tenant with id={tenant_id} not found")
                return JsonResponse({"error": "Invalid tenant_id"}, status=400)

            reference = str(uuid.uuid4())

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
                    "tenant_id": data['tenant_id'],
                    "unit_id" : data['unit_id'],
                }
            }

            headers = {
                'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }

            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                json=payload
            )
            res_data = response.json()

            if res_data.get('status'):
                Payment.objects.create(
                    email=data['email'],
                    amount=data['amount'],
                    phone=data['phone'],
                    provider=data['provider'],
                    reference=reference,
                    tenant=tenant.phoneNo,
                    unit=tenant.unit.room_number
                )
                logger.info(f"Payment initialized and saved: ref={reference}")
                return JsonResponse(res_data)
            else:
                logger.error("Payment initialization failed with Paystack")
                return JsonResponse({"error": "Payment initialization failed"}, status=400)

        except json.JSONDecodeError:
            logger.exception("Invalid JSON format")
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            logger.exception("Unexpected error during payment initialization")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def verify_payment(request, reference):
    logger.info(f"Verifying payment with reference: {reference}")

    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
    }

    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    res_data = response.json()

    if res_data.get('status'):
        data = res_data['data']
        logger.info(f"Verification success: {data}")

        # Update payment status in DB
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = data['status']  # likely "success"
            payment.channel = data['channel']
            payment.save()
            logger.info(f"Updated payment status for reference {reference}")
        except Payment.DoesNotExist:
            logger.warning(f"Payment with reference {reference} not found in DB")

        return JsonResponse({
            "status": True,
            "message": f"Payment was {data['status']}",
            "data": data
        })
    else:
        logger.error(f"Verification failed: {res_data}")
        return JsonResponse({
            "status": False,
            "message": "Payment verification failed",
            "data": res_data
        }, status=400)
