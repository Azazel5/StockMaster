from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import CompanyModel, CompanyStockInformation
from .serializers import CompanyModelSerializer, CompanyStockInformationSerializer
from .permissions import IsAuthenticatedSuperuser 


class CompanyViewSet(viewsets.ModelViewSet):
# Model viewset for the company model 
# -------------------------------------------
# Overriden create function for this viewset to 
# support multiple PUTs in the API, so it allows 
# a list of JSON to be added  

    queryset = CompanyModel.objects.all().order_by('id')
    serializer_class = CompanyModelSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def create(self, request, pk=None):
        is_many = True if isinstance(request.data, list) else False 
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CompanyInformationViewSet(viewsets.ModelViewSet):
# A viewset for the company information. 
# ----------------------------------------------------------------------
# It supports a query parameter where you can type in the  
# company name to return a list of stocks of that company. url/stock/?company=...
# Similar overrided create function to allow multiple PUTs in the API 

    queryset = CompanyStockInformation.objects.all().order_by('id')
    serializer_class = CompanyStockInformationSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def create(self, request, pk=None):
        is_many = True if isinstance(request.data, list) else False 
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if 'company' in self.request.query_params:
            company_name = self.request.query_params.get('company', None)
            company = CompanyModel.objects.get(company_name=company_name)
            self.queryset = CompanyStockInformation.objects.filter(company=company).order_by('id')            
        return self.queryset

class CompanyMaximumTransactionView(viewsets.ReadOnlyModelViewSet):
# API endpoint to order the stocks by amount. Later I will use this to support 
# date ranges and only return the top 123 companies for that daterange, and is 
# why I decided to make this an endpoint instead of just querying the model.
    queryset = CompanyStockInformation.objects.all().order_by('-amount')
    serializer_class = CompanyStockInformationSerializer

            


