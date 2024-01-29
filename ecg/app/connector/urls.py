from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/ecg_monitoring',
        views.ECGView.as_view({'post': 'create'}),
        name='ecg_monitoring',
    ),
    path(
        'api/ecg_monitoring/<str:ecg_id>',
        views.ECGView.as_view({'get': 'retrieve'}),
        name='ecg_monitoring',
    ),
    path('api/login/', views.UserLoginView.as_view(), name='api-login'),
    path('api/registration/', views.UserRegistrationView.as_view(), name='api-register'),
]
