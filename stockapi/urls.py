from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyStaticSet,
    CompanyDynamicSet,
    StockSet
)

router = DefaultRouter()
router.register('company-static', CompanyStaticSet)
router.register('company-dynamic', CompanyDynamicSet)
router.register('stock', StockSet)

urlpatterns = [
    path('', include(router.urls))
]