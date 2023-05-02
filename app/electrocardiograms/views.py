"""
Views for the ecgs APIs
"""

from rest_framework import viewsets


from core.models import Electrocardiogram
from electrocardiograms import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ElectrocardiogramViewSet(viewsets.ModelViewSet):
    """View for manage ecg APIs."""
    serializer_class = serializers.ElectrocardiogramSerializer
    queryset = Electrocardiogram.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """Retrieve ecgs for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new ecg."""
        serializer.save(user=self.request.user)
