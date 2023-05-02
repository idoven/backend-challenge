"""
URL mappings for the user API
"""

from django.urls import path

from users import views

app_name = 'users'


urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token')
]
