from rest_framework import serializers 
from .models import CompanyModel 

class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ['id', 'company_name']