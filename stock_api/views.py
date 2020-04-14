from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import CompanyModel, CompanyStockInformation
from .serializers import CompanyModelSerializer, CompanyStockInformationSerializer
from .permissions import IsAuthenticatedSuperuser 


class CompanyViewSet(viewsets.ModelViewSet):
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

# A viewset for the company information. It supports a query parameter 'company' where you can type in the 
# company name to return a list of stocks of that company. 
class CompanyInformationViewSet(viewsets.ModelViewSet):
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
    queryset = CompanyStockInformation.objects.all().order_by('-amount')
    serializer_class = CompanyStockInformationSerializer

            


