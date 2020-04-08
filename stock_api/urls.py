from django.urls import path
from stock_api import views 
from rest_framework.urlpatterns import format_suffix_patterns 

urlpatterns = [
    path('company/', views.CompanyList.as_view()),
    path('company/<int:pk>/', views.CompanyDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)