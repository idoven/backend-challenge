from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Electrocardiogram, Lead

from electrocardiograms.serializers import ElectrocardiogramSerializer


ELECTROCARDIOGRAMS_URL = reverse('ecgs:ecg-list')


def detail_url(electrocardiogram_id):
    """Create and return a electrocardiogram detail URL."""
    return reverse('ecgs:ecg-detail', args=[electrocardiogram_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_lead(**params):
    """Create and return a sample electrocardiogram."""
    defaults = {
        'name': 'Sample electrocardiogram name',
        'samples': 3,
        'signal': [0, 1, 2]
    }

    defaults.update(params)

    lead = Lead.objects.create(**defaults)
    return lead


def create_electrocardiogram(**params):
    """Create and return a sample electrocardiogram."""
    defaults = {}
    defaults.update(params)

    electrocardiogram = Electrocardiogram.objects.create(**defaults)
    return electrocardiogram


class PublicElectrocardiogramAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ELECTROCARDIOGRAMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateElectrocardiogramApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_create_electrocardiogram(self):
        """Test creating a electrocardiogram."""
        payload = {
            'leads': [
                {
                    'name': 'Sample electrocardiogram name',
                    'samples': 3,
                    'signal': [0, 1, 2]
                }
            ]
        }
        res = self.client.post(ELECTROCARDIOGRAMS_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        electrocardiogram = Electrocardiogram.objects.get(id=res.data.get('id'))
        serializer = ElectrocardiogramSerializer(electrocardiogram)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(electrocardiogram.user, self.user)

    def test_retrieve_electrocardiograms(self):
        """Test retrieving a list of electrocardiograms."""
        electrocardiogram = create_electrocardiogram(user=self.user)
        create_lead(electrocardiogram=electrocardiogram)
        electrocardiogram_2 = create_electrocardiogram(user=self.user)
        create_lead(electrocardiogram=electrocardiogram_2)

        res = self.client.get(ELECTROCARDIOGRAMS_URL)

        electrocardiograms = Electrocardiogram.objects.all().order_by('-id')
        serializer = ElectrocardiogramSerializer(electrocardiograms, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_electrocardiogram_list_limited_to_user(self):
        """Test list of electrocardiograms is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        electrocardiogram = create_electrocardiogram(user=self.user)
        create_lead(electrocardiogram=electrocardiogram)
        electrocardiogram_2 = create_electrocardiogram(user=other_user)
        create_lead(electrocardiogram=electrocardiogram_2)

        res = self.client.get(ELECTROCARDIOGRAMS_URL)

        electrocardiograms = Electrocardiogram.objects.filter(user=self.user)
        serializer = ElectrocardiogramSerializer(electrocardiograms, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_electrocardiogram_detail(self):
        """Test get electrocardiogram detail."""
        electrocardiogram = create_electrocardiogram(user=self.user)
        create_lead(electrocardiogram=electrocardiogram)

        url = detail_url(electrocardiogram.id)
        res = self.client.get(url)

        serializer = ElectrocardiogramSerializer(electrocardiogram)
        self.assertEqual(res.data, serializer.data)
