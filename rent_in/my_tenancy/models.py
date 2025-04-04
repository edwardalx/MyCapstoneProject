from django.db import models
from accounts.models import Tenant
from my_properties.models import Property, Unit
from dateutil.relativedelta import relativedelta

class Tenancy_Agreement(models.Model):
    contract_start_date = models.DateField(blank=False, null=False)
    contract_duration = models.IntegerField(help_text="Duration in months")
    contract_end_date = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenancy_agreements')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='tenancy_agreements')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenancy_agreements')
    total_amount_paid = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.contract_start_date and self.contract_duration:
            self.contract_end_date = self.contract_start_date + relativedelta(months=self.contract_duration)
        super().save(*args, **kwargs)

    
    def amount_left(self):
        if self.total_amount_paid is not None and self.unit.cost is not None:
            return self.unit.cost - self.total_amount_paid
        return None

    def __str__(self):
        return f"Tenant: {self.tenant.first_name} Contract End: {self.contract_end_date} Amount Left: {self.amount_left()}"
