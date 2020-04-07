from django.contrib import admin
from .models import CompanyModel, CompanyStockInformation

admin.site.register(CompanyModel)
admin.site.register(CompanyStockInformation)