from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import CompanyModel
from .serializers import CompanyModelSerializer

@csrf_exempt
def company_list(request):
    if request.method == 'GET':
        objects = CompanyModel.objects.all() 
        serializer = CompanyModelSerializer()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanyModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)