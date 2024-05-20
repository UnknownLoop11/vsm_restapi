import random
from rest_framework import serializers

from main.models import Store, Location, Customer, OrderDetails, File, Pricing
from phonenumber_field.serializerfields import PhoneNumberField


def get_randint():
    num = random.randint(1, 999)
    return num


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'



class StoreSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    pricing = PricingSerializer()

    class Meta:
        model = Store
        model_fields = [field.name for field in model._meta.fields]

        fields = model_fields + ['pricing', 'location']


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    order = OrderDetailsSerializer()

    class Meta:
        model = Customer
        model_fields = [field.name for field in model._meta.fields]
        fields = model_fields + ['order', 'store']


class StoreRegisterSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    store_name = serializers.CharField(required=True)
    owner = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    contact_no = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    lat = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    long = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    pricing = serializers.JSONField(required=True)
    gmap_link = serializers.URLField(required=True)

    def create(self, validated_data):
        location_instance = Location.objects.create(
            address=validated_data.get('address'),
            lat=validated_data.get('lat'),
            long=validated_data.get('long')
        )
        pricing_instance = Pricing.objects.create(
            normal=validated_data.get('pricing')['one_side'][0],
            color=validated_data.get('pricing')['one_side'][1],
            normal_2side=validated_data.get('pricing')['double_side'][0],
            color_2side=validated_data.get('pricing')['double_side'][1],
        )
        store_instance = Store.objects.create(
            uid=validated_data['uid'],
            store_name=validated_data.get('store_name'),
            owner=validated_data.get('owner'),
            description=validated_data.get('description'),
            email=validated_data.get('email'),
            contact_no=validated_data.get('contact_no'),
            location=location_instance,
            pricing=pricing_instance,
            gmap_link=validated_data.get('gmap_link')
        )

        return validated_data


class StoreParameters(serializers.Serializer):
    uid = serializers.CharField(required=True)
    ref_id = serializers.IntegerField(required=False)
    lat = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    long = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    rad = serializers.IntegerField(required=False)


class StoreProfileUpdate(serializers.Serializer):
    store_name = serializers.CharField(required=False)
    owner = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    contact_no = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    lat = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    long = serializers.DecimalField(max_digits=20, decimal_places=16, required=False)
    gmap_link = serializers.URLField(required=False)

    def update(self, instance, validated_data):
        instance.store_name = validated_data.get('store_name', instance.store_name)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.description = validated_data.get('description', instance.description)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_no = validated_data.get('contact_no', instance.contact_no)
        instance.location.address = validated_data.get('address', instance.location.address)
        instance.location.lat = validated_data.get('lat', instance.location.lat)
        instance.location.long = validated_data.get('long', instance.location.long)
        instance.gmap_link = validated_data.get('gmap_link', instance.gmap_link)
        instance.save()
        return validated_data


class StoreOrderSerializer(serializers.Serializer):
    store_uid = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    contact_no = PhoneNumberField(required=True, region='IN')
    xerox_type = serializers.CharField(required=True)
    copies = serializers.IntegerField(required=True)
    files = serializers.ListField(child=serializers.FileField(), required=True)

    def create(self, validated_data):
        store = Store.objects.get(uid=validated_data.get('store_uid'))

        order_details = OrderDetails.objects.create(
            type=validated_data.get('xerox_type'),
            copies=validated_data.get('copies'),
        )

        customer = Customer.objects.create(
            store=store,
            reference_id=get_randint(),
            name=validated_data.get('name'),
            contact_no=validated_data.get('contact_no'),
            order=order_details
        )

        for file in validated_data.get('files'):
            file = File.objects.create(
                order=customer,
                file=file
            )

        return validated_data


class OrderUpdate(serializers.Serializer):
    status = serializers.BooleanField(required=False)
    accepted = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):

        instance.status = validated_data.get('status', instance.status)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.save()
        return validated_data

class GetLocationParams(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)
