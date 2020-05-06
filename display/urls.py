from django.contrib import admin
from django.urls import path, include
from .views import SetDisplay, Scrape

urlpatterns = [
    path('', SetDisplay.as_view(), name='display_home'),
    path('scrape/', Scrape.as_view(), name='display_scrape')
]