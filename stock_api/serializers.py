from rest_framework import serializers 
from .models import CompanyModel, CompanyStockInformation

class CompanyModelSerializer(serializers.ModelSerializer):
# Company model serializer to be user in views.py later 
# -----------------------------------------------------
# Overriden create function to make sure duplicate companies 
# aren't created 
    company_id = serializers.CharField(source='id', read_only=True)
    class Meta:
        model = CompanyModel
        fields = ['company_id', 'company_name']

    def create(self, validated_data):
        company, created = CompanyModel.objects.get_or_create(**validated_data)
        return company 

class CompanyStockInformationSerializer(serializers.ModelSerializer):
# A nested serializer for the stock information, nested with the CompanyModelSerializer.
# ------------------------------------------------------------------------------------------------------------
# It creates the company if it isn't listed and adds the stock to the existing company if it does. 
# Json structure is: {stock_id, {CompanyModelSerializer}, other fields...}

    company = CompanyModelSerializer()
    class Meta:
        model = CompanyStockInformation
        fields = [
            'id', 'company', 'number_of_transactions',
            'maximum', 'minimum', 'closing', 'traded_shares',
            'amount', 'previous_closing', 'difference_rs', 'date_added'
        ]
    
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = CompanyModel.objects.get_or_create(**company_data)
        stock, created = CompanyStockInformation.objects.get_or_create(company=company, **validated_data)
        return stock
