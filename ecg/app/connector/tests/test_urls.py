from django.test import TestCase
from django.urls import resolve


class TestUrls(TestCase):
    def test_ecg_monitoring_url(self):
        resolver = resolve('/api/ecg_monitoring')
        self.assertEqual(resolver.view_name, 'ecg_monitoring')

    def test_ecg_monitoring_zero_crossing_url(self):
        resolver = resolve('/api/ecg_monitoring/zero_crossing/1')
        self.assertEqual(resolver.view_name, 'ecg_monitoring')

    def test_login_url(self):
        resolver = resolve('/api/login/')
        self.assertEqual(resolver.view_name, 'api_login')

    def test_registration_url(self):
        resolver = resolve('/api/registration/')
        self.assertEqual(resolver.view_name, 'api_register')
