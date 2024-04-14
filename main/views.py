from django.http import HttpResponse
from django.shortcuts import render

import json


# Create your views here.


def test(request):
    # if request.method == 'POST':
    #     data = {
    #         'name': request.POST['name'],
    #         'files': request.FILES.getlist('file')
    #     }
    #     print(data)
    #     decode = json.dumps(data)
    #     print(decode)
    # if request.method == 'POST':
    #     try:
    #         # Create a Man instance
    #         user = Man.objects.create(name=request.POST['name'])
    #
    #         # Handle multiple file uploads
    #         uploaded_files = request.FILES.getlist('file')  # Use getlist() to handle multiple files
    #
    #         # Create a File instance for each uploaded file
    #         for uploaded_file in uploaded_files:
    #             File.objects.create(file=uploaded_file, man=user)
    #     except Exception as e:
    #         # Handle exceptions, such as form validation errors or database errors
    #         print(e)

    return render(request, 'test.html')


def home(request):
    return HttpResponse('<h1 style="{margin: auto:}">Welcome to Prerox Rest-Api</h1>')
