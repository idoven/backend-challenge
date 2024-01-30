from django.urls import path

from . import views

urlpatterns = [
    path(
        'ecg_monitoring',
        views.ECGView.as_view({'post': 'create', 'put': 'update'}),
        name='ecg_monitoring',
    ),
    path(
        'ecg_monitoring/<str:ecg_id>',
        views.ECGView.as_view({'get': 'retrieve', 'delete': 'delete'}),
        name='ecg_monitoring',
    ),
    path(
        'ecg_monitoring/zero_crossing/<str:ecg_id>',
        views.ECGView.as_view({'get': 'retrieve_zero_crossing'}),
        name='ecg_monitoring',
    ),
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='api_login',
    ),
    path(
        'registration/',
        views.UserRegistrationView.as_view(),
        name='api_register',
    ),
]
