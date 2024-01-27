from django.urls import path

from . import views

urlpatterns = [
    path(
        'ecg_monitoring',
        views.ECGView.as_view({'get': 'retrieve', 'post': 'create'}),
        name='ecg_monitoring',
    ),
]
