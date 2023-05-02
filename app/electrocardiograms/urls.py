
"""
URL mappings for the ecgs app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from electrocardiograms import views


router = DefaultRouter()
router.register('ecgs', views.ElectrocardiogramViewSet, basename='ecg')


app_name = 'ecgs'

urlpatterns = [
    path('', include(router.urls)),
]
