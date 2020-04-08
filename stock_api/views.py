from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404

from .models import CompanyModel
from .serializers import CompanyModelSerializer
from .permissions import IsAuthenticatedSuperuser 


class CompanyList(generics.ListCreateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = (IsAuthenticatedSuperuser,)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = (IsAuthenticatedSuperuser,)

