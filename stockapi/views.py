from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    ModelCompany,
    ModelDynamicInfo,
    ModelStock
)
from .serializers import (
    ModelCompanySerializer,
    ModelDynamicSerializer,
    ModelStockSerializer
)

from rest_framework.response import Response
from .permissions import IsAuthenticatedSuperuser 

class CompanyStaticSet(viewsets.ModelViewSet):
# Model viewset for the company model 
# -------------------------------------------
# Overriden create function for this viewset to 
# support multiple PUTs in the API, so it allows 
# a list of JSON to be added  

    queryset = ModelCompany.objects.all().order_by('id')
    serializer_class = ModelCompanySerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CompanyDynamicSet(viewsets.ModelViewSet):
# A viewset for the company's dynamic information. 
# ----------------------------------------------------------------------
# Similar overriden create function to allow multiple PUTs in the API 

    queryset = ModelDynamicInfo.objects.all().order_by('id')
    serializer_class = ModelDynamicSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StockSet(viewsets.ModelViewSet):
# A viewset for the stock information. 
# ----------------------------------------------------------------------
# Similar overriden create function to allow multiple PUTs in the API 

    queryset = ModelStock.objects.all().order_by('id')
    serializer_class = ModelStockSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
