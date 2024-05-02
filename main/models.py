import os

import googlemaps
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

from vsm_restapi import settings


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


# Create your models here.
gmap = googlemaps.Client(key=settings.G_API_KEY)

class Location(models.Model):
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=20, decimal_places=16)
    long = models.DecimalField(max_digits=20, decimal_places=16)
    def fill_cords(self, addrs):
        coords = gmap.geocode(addrs)
        if coords:
            location = coords[0]['geometry']['location']
            self.lat = float(location['lat'])
            self.long = float(location['lng'])
    def save(self, *args, **kwargs):

        if not (self.lat and self.long):
            self.fill_cords(self.address)

        super().save(*args, **kwargs)


class Pricing(models.Model):
    normal = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.DecimalField(max_digits=5, decimal_places=2)
    normal_2side = models.DecimalField(max_digits=5, decimal_places=2)
    color_2side = models.DecimalField(max_digits=5, decimal_places=2)


class Store(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    store_name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    contact_no = PhoneNumberField(region='IN')
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    pricing = models.OneToOneField(Pricing, on_delete=models.CASCADE)
    gmap_link = models.URLField()

    def __str__(self):
        return self.store_name



    def delete(self, *args, **kwargs):
        location_instance = Location.objects.get(id=self.location.id)
        pricing_instance = Pricing.objects.get(id=self.pricing.id)
        super().delete(*args, **kwargs)
        location_instance.delete()
        pricing_instance.delete()


class StoreImage(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/')


class OrderDetails(models.Model):
    type = models.CharField(max_length=50)
    copies = models.PositiveIntegerField()
    uploaded_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)
    accepted = models.BooleanField(null=True)

    def __str__(self):
        try:
            obj = Customer.objects.get(order_id=self.id)
            return f"{obj.reference_id}, {obj.name}"
        except Customer.DoesNotExist:
            return f"Unknown Order"


class Customer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    reference_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    contact_no = PhoneNumberField(region='IN')
    order = models.OneToOneField(OrderDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        order_instance = OrderDetails.objects.get(id=self.order.id)
        super().delete(*args, **kwargs)
        order_instance.delete()


class File(models.Model):
    order = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=5, null=True)


@receiver(post_delete, sender=File)
def delete_file_on_delete(sender, instance, **kwargs):
    # Delete the file when the record is deleted
    delete_file(instance.file.path)


@receiver(post_delete, sender=StoreImage)
def delete_file_on_delete(sender, instance, **kwargs):
    # Delete the file when the record is deleted
    delete_file(instance.image.path)
