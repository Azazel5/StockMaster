from django.urls import path, include
from stock_api import views 
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('stock', views.CompanyInformationViewSet, basename='stock')
router.register('max-transacation-amount', views.CompanyMaximumTransactionView)

urlpatterns = [
    path('', include(router.urls)),
]
