from django.db import models
from accounts.models import Tenant
from my_tenancy.models import Tenancy_Agreement
# Create your models here.
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    tenancy_agreement = models.ForeignKey('my_tenancy.Tenancy_Agreement', on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.IntegerField(blank=True, null=True)
    amount_left = models.IntegerField(blank=True, null=True)
    total_amount_paid = models.IntegerField(blank=True, null=True)
    first_payment_date = models.DateField(auto_now=True)
    last_payment_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount_paid = self.tenancy_agreement.payments.aggregate(models.Sum('amount_paid'))['amount_paid__sum']
        self.amount_left =  self.tenancy_agreement.unit.cost - self.total_amount_paid 
        super().save(*args, **kwargs)

        # Update the Tenancy_Agreement's amount_paid after saving the payment
        self.tenancy_agreement.total_amount_paid = self.total_amount_paid 
        self.tenancy_agreement.save()
    def __str__(self):
        return f"{self.tenant.user.first_name} Amount Paid: {self.amount_paid} 'Amount Left:{self.amount_left}"