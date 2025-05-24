from django.db import models

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    image_url = models.URLField(max_length=500,)
    no_of_units = models.IntegerField(blank=True, null=True)
    no_of_floors = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField()

    def __str__(self):
        return f"Property: {self.name}"

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    floor = models.IntegerField()
    room_number = models.CharField(max_length=14, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    max_no_of_people = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['property', 'room_number'], name='unique_unit_per_property')
        ]

    def __str__(self):
        return f"Unit {self.room_number} in {self.property.name}"

class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    description = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='properties_images/')

    def __str__(self):
        return f"Image for {self.property or self.unit}"