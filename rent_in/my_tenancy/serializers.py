from rest_framework import serializers
from .models import Tenancy_Agreement
from my_properties.serializers import PropertySerialzer, UnitSerialzer
from accounts.serializers import TenantSerializer
from my_properties.models import Property
from accounts.models import Tenant

class TenancySerialzer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only = True)
    property = PropertySerialzer(read_only =True)
    unit = UnitSerialzer(read_only = True)

    class Meta:
        model = Tenancy_Agreement
        fields = '__all__'
    def create(self, validated_data):
        username_data = validated_data.pop('username')
        property_data = validated_data.pop('property_name')

        # Get or create the property instance
        property_instance, _ = Property.objects.get_or_create(**property_data)

        # Create the tenancy agreement
        tenancy_agreement = Tenancy_Agreement.objects.create(property_name=property_instance, **validated_data)

        # Add tenants to ManyToMany field
        for tenant_data in username_data:
            tenant, _ = Tenant.objects.get_or_create(**tenant_data)
            tenancy_agreement.username.add(tenant)

        return tenancy_agreement

    def update(self, instance, validated_data):
        username_data = validated_data.pop('phone_no', None)
        property_data = validated_data.pop('property_name', None)

        # Update property if provided
        if property_data:
            property_instance, _ = Property.objects.get_or_create(**property_data)
            instance.property_name = property_instance

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ManyToMany phone_no field
        if username_data is not None:
            instance.username_data.clear()  # Remove existing tenants
            for tenant_data in username_data:
                tenant, _ = Tenant.objects.get_or_create(**tenant_data)
                instance.username.add(tenant)
        return instance
