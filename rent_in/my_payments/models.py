from django.db import models
from accounts.models import Tenant
from my_properties.models import Unit # Update this import to your actual app name
from my_tenancy.models import Tenancy_Agreement
# Create your models here.


class Payment(models.Model):
    email = models.EmailField(default='example@example.com')
    amount = models.IntegerField(help_text="Amount in pesewas", default=0)  # e.g. 5000 = GHS 50.00
    currency = models.CharField(max_length=5, default='GHS')
    phone = models.CharField(max_length=15)
    provider = models.CharField(max_length=20, choices=[
        ('mtn', 'MTN'),
        ('vodafone', 'Vodafone'),
        ('airteltigo', 'AirtelTigo')
    ])
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="pending")
    channel = models.CharField(max_length=30, default='mobile_money')
    created_at = models.DateTimeField(auto_now_add=True)

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="payments")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.email} - {self.amount} GHS - {self.status}"



class PaymentSummary(models.Model):
    tenancy_agreement = models.OneToOneField(Tenancy_Agreement, on_delete=models.CASCADE, related_name="payment_summary")
    total_amount_paid = models.IntegerField(default=0)
    amount_left = models.IntegerField(default=0)
    last_payment_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount_paid = self.tenancy_agreement.payments.aggregate(
            models.Sum('amount')
        )['amount__sum'] or 0

        self.amount_paid = self.payment.amount
        self.amount_left = self.tenancy_agreement.unit.cost - self.total_amount_paid
        super().save(*args, **kwargs)

        self.tenancy_agreement.total_amount_paid = self.total_amount_paid
        self.tenancy_agreement.save()

    def __str__(self):
        return f"{self.tenant.user.first_name} - Paid: {self.amount_paid} - Left: {self.amount_left}"