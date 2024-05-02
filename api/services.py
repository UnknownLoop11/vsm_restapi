import googlemaps
from haversine import haversine, Unit

from main.models import Store, Customer
from api.serializers import StoreSerializer
from vsm_restapi import settings

gmap = googlemaps.Client(key=settings.G_API_KEY)


class Services:
    def __init__(self):
        pass

    def get_loc(self, lat, long):
        loc = gmap.reverse_geocode((lat, long))
        return loc[0]['formatted_address']

    def get_store(self, uid):
        try:
            store = Store.objects.get(uid=uid)
            serializer = StoreSerializer(store)
        except:
            return {'error': 'Invalid user id provided.'}

        return serializer.data

    def get_store_list(self, **kwargs):
        params = ['lat', 'long', 'rad']
        stores_list = {}
        count = 0

        if kwargs:

            if all(key in kwargs for key in params):
                coords, rad = (float(kwargs.get('lat')), float(kwargs.get('long'))), float(kwargs.get('rad'))
                stores = Store.objects.all()

                for store in stores:
                    distance = haversine(coords, (store.location.lat, store.location.long), unit=Unit.METERS)
                    if distance <= rad:
                        serializer = StoreSerializer(store).data
                        serializer.update({'distance': round(distance, 2), 'unit': 'meters(m)'})
                        stores_list[count] = serializer
                        count += 1
                return stores_list
        else:
            return {"error": "Error occurred."}


class CustomResponse:
    def __init__(self):
        pass

    __responses = {
        'registered': {
            'success': 'Your store has been registered successfully.'
        }, 'error': {
            'error': 'Provide Query Parameters to fetch data.'
        }

    }

    def get_response(self, context):
        return self.__responses.get(context)


