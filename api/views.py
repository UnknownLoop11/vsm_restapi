import zipfile, io

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import StoreSerializer, CustomerSerializer, StoreRegisterSerializer, StoreParameters, \
    StoreProfileUpdate, StoreOrderSerializer, OrderUpdate, StoreImageSerializer
from main.models import Store, Customer, File, StoreImage
from api.services import Services, CustomResponse

services = Services()
response = CustomResponse()


# Function-Based Views

@api_view(['POST'])
def register_store(request):
    serializer = StoreRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(response.get_response('registered'), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_stores(request):
    params = request.query_params
    if params:
        store_list = services.get_store_list(lat=params['lat'], long=params['long'], rad=params['rad'])
        return Response(store_list, status=status.HTTP_200_OK)
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_store_orders(request):
    params = StoreParameters(data=request.query_params)
    if params.is_valid():
        uid = params.validated_data.get('uid')  # User id
        orders = Customer.objects.filter(store__uid=uid)
        serializer = CustomerSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response


@api_view(['GET'])
def generate_files(request, ref_id):
    name = Customer.objects.get(reference_id=ref_id)
    file_paths = [f"media/{file_path.file}" for file_path in File.objects.filter(order__reference_id=ref_id)]
    # Create a zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for file_path in file_paths:
            file_name = str(file_path[8:])
            zipf.write(file_path, arcname=file_name)
    # Create the HttpResponse with the zip file
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{name.name}.zip"'
    return response

@api_view(['GET'])
def get_store_images(request):
    params = StoreParameters(data=request.query_params)
    if params.is_valid():
        uid = params.validated_data.get('uid')  # User id
        images = StoreImage.objects.filter(store__uid=uid)
        serializer = StoreImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response


# Class-Based Views
class StoreProfile(APIView):

    def get(self, request):
        params = StoreParameters(data=request.query_params)  # For query params
        if params.is_valid():
            uid = params.validated_data.get('uid')  # User id
            obj = services.get_store(uid)
            return Response(obj, status=status.HTTP_201_CREATED)

        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        params = StoreParameters(data=request.query_params)
        if params.is_valid():
            obj = get_object_or_404(Store, uid=params.validated_data.get('uid'))
            serializer = StoreProfileUpdate(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        params = StoreParameters(data=request.query_params)
        if params.is_valid():
            obj = get_object_or_404(Store, uid=params.validated_data.get('uid'))
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreOrder(APIView):

    def get(self, request):
        params = StoreParameters(data=request.query_params)  # For query params
        if params.is_valid():
            uid = params.validated_data.get('uid')
            ref_id = params.validated_data.get('ref_id')
            order = get_object_or_404(Customer, reference_id=ref_id, store__uid=uid)
            serializer = CustomerSerializer(order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        params = StoreParameters(data=request.query_params)
        if params.is_valid():
            serializer = StoreOrderSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                # print(serializer.data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        params = StoreParameters(data=request.query_params)
        if params.is_valid():
            uid = params.validated_data.get('uid')
            ref_id = params.validated_data.get('ref_id')
            order = get_object_or_404(Customer, reference_id=ref_id, store__uid=uid).order
            serializer = OrderUpdate(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        params = StoreParameters(data=request.query_params)
        if params.is_valid():
            uid = params.validated_data.get('uid')
            ref_id = params.validated_data.get('ref_id')
            order = get_object_or_404(Customer, reference_id=ref_id, store__uid=uid)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(params.errors, status=status.HTTP_400_BAD_REQUEST)
