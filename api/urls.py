
from django.urls import path

from api.views import register_store, get_stores, get_store_orders, generate_files, get_store_images
from api.views import StoreProfile, StoreOrder


urlpatterns = [
    path('store/register/', register_store, name='store_registration'),  # POST
    path('store', StoreProfile.as_view(), name='store_profile'),  # GET, PUT, DELETE
    path('store/list', get_stores, name='store_list'),  # GET
    path('store/order', StoreOrder.as_view(), name='store_view'),  # POST, GET, PUT, DELETE
    path('store/order/list', get_store_orders, name="store_orders_list"),  # GET
    path('store/order/download/<int:ref_id>', generate_files, name='download_files'),
    path('store/images', get_store_images, name="store_image")
]