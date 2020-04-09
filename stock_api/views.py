from rest_framework import viewsets

from .models import CompanyModel, CompanyStockInformation
from .serializers import CompanyModelSerializer, CompanyStockInformationSerializer
from .permissions import IsAuthenticatedSuperuser 


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all().order_by('id')
    serializer_class = CompanyModelSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def perform_create(self, serializer):
        serializer.save()

# A viewset for the company information. It supports a query parameter 'company' where you can type in the 
# company name to return a list of stocks of that company. 
class CompanyInformationViewSet(viewsets.ModelViewSet):
    queryset = CompanyStockInformation.objects.all().order_by('id')
    serializer_class = CompanyStockInformationSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

    def get_queryset(self):
        queryset = CompanyStockInformation.objects.all()
        company_name = self.request.query_params.get('company', None)
        if company_name is not None:
            company = CompanyModel.objects.get(company_name=company_name)
            queryset = CompanyStockInformation.objects.filter(company=company)
        return queryset
            


