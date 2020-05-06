from rest_framework import serializers 
from .models import (
    ModelCompany,
    ModelDynamicInfo,
    ModelStock
)

class ModelCompanySerializer(serializers.ModelSerializer):
# Company model serializer to be user in views.py later 
# -----------------------------------------------------
# Overriden create function to make sure duplicate companies 
# aren't created 

    company_id = serializers.CharField(source='id', read_only=True)
    class Meta:
        model = ModelCompany
        fields = ['company_id','company_symbol', 'company_name']
        
    def create(self, validated_data):
        company, create = ModelCompany.objects.get_or_create(**validated_data)
        return company

class ModelDynamicSerializer(serializers.ModelSerializer):
# A nested serializer for the company's dynamic information, nested with the ModelCompanySerializer.
# ----------------------------------------------------------------------------------------------------
# It creates the company if it isn't listed and adds the stock to the existing company if it does. 
# Json structure is: {stock_id, {ModelCompanySerializer}, other fields...}

    company = ModelCompanySerializer()
    class Meta:
        model = ModelDynamicInfo
        fields = [
            'id', 'company', 'latest_bonus_share', 
            'latest_cash_dividend', 'year', 
            'book_close_date'
        ]
        
    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = ModelCompany.objects.get_or_create(**company_data)
    
        dynamic, create = ModelDynamicInfo.objects.get_or_create(company=company, **validated_data)
        return dynamic 

class ModelStockSerializer(serializers.ModelSerializer):
# A nested serializer for the stock information, nested with the ModelCompanySerializer.
# ------------------------------------------------------------------------------------------------
# It creates the company if it isn't listed and adds the stock to the existing company if it does. 
# Json structure is: {stock_id, {ModelCompanySerializer}, other fields...}

    company = ModelCompanySerializer()
    class Meta:
        model = ModelStock
        fields = [
            'id', 'company', 'conf', 'open_price',
            'high', 'low', 'close', 'vwap', 
            'volume', 'prev_close', 'turnover',
            'trans', 'difference_rs', 'range_rs', 
            'difference_percent', 'range_percent',
            'vwap_percent', 'oneeighty_days',
            'fiftytwo_week_high', 'fiftytwo_week_low',
            'date_added'
        ]

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, created = ModelCompany.objects.get_or_create(**company_data)

        stock, create = ModelStock.objects.get_or_create(company=company, **validated_data)
        return stock