from django.contrib import admin
from django.urls import path, include
from .views import set_display, scrape_data

urlpatterns = [
    path('', set_display, name='display_home'),
    path('scrape/', scrape_data, name='display_scrape')
]