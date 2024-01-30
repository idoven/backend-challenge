from django.test import TestCase
from rest_framework.test import APIRequestFactory

from connector.models import UserModel
from connector.serializers import (
    ECGModelSerializer,
    ECGResponseSerializer,
    LeadsSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)


class UserLoginSerializerTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPassword123!',
        )
        self.user_data = {
            'username': 'testuser',
            'password': 'TestPassword123!',
        }

    def tearDown(self):
        # Clean up created users
        UserModel.objects.all().delete()

    def test_valid_login_with_username(self):
        data = {'username': 'testuser', 'password': 'TestPassword123!'}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('user', serializer.validated_data)

    def test_invalid_login_with_email(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_login_missing_password(self):
        data = {'username': 'testuser'}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_invalid_login_missing_username_and_password(self):
        data = {}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    #
    def test_invalid_login_wrong_credentials(self):
        data = {'username': 'testuser', 'password': 'WrongPassword'}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)


class UserRegistrationSerializerTests(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'TestPassword123!',
            'first_name': 'name',
            'last_name': 'last_name',
        }

    def test_valid_registration_data(self):
        serializer = UserRegistrationSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'testuser')

    def test_short_password(self):
        data = self.user_data.copy()
        data['password'] = 'Pass'
        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_missing_uppercase_letter(self):
        data = self.user_data.copy()
        data['password'] = 'password!'

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_missing_special_character(self):
        data = self.user_data.copy()
        data['password'] = 'MissingSpecialChar123'

        serializer = UserRegistrationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_password_hashing(self):
        serializer = UserRegistrationSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid())
        saved_user = serializer.save()

        self.assertNotEqual(saved_user.password, 'TestPassword123!')
        self.assertTrue(saved_user.check_password('TestPassword123!'))


class LeadsSerializerTests(TestCase):
    def setUp(self) -> None:
        self.signal = '[1, 2, 3, -4, 2, -6, -4.3, 4.2]'
        self.num_samples = 10
        self.name = 'I'

    def test_leads_serializer_valid_data(self):
        data = {
            'name': self.name,
            'num_samples': self.num_samples,
            'signal': self.signal,
        }

        serializer = LeadsSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], self.name)
        self.assertEqual(
            serializer.validated_data['num_samples'],
            self.num_samples,
        )
        self.assertEqual(serializer.validated_data['signal'], self.signal)

    def test_leads_serializer_missing_required_field(self):
        # Test with missing 'name' field
        data = {'num_samples': self.num_samples, 'signal': self.signal}

        serializer = LeadsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_leads_serializer_invalid_choice(self):
        # Test with invalid 'name' choice
        data = {
            'name': 'InvalidLead',
            'num_samples': self.num_samples,
            'signal': self.signal,
        }

        serializer = LeadsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_leads_serializer_invalid_num_samples(self):
        # Test with invalid 'num_samples' type
        data = {
            'name': self.name,
            'num_samples': 'invalid',
            'signal': self.signal,
        }

        serializer = LeadsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('num_samples', serializer.errors)

    def test_leads_serializer_invalid_signal_format(self):
        # Test with invalid 'signal' format
        data = {
            'name': self.name,
            'num_samples': self.num_samples,
            'signal': 'invalid',
        }

        serializer = LeadsSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('signal', serializer.errors)


class ECGModelSerializerTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/ecg_monitoring/')
        self.request.user = self.user

    def tearDown(self):
        # Clean up created users
        UserModel.objects.all().delete()

    def test_ecg_model_serializer(self):
        leads_data = [
            {'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4,2,-6]'},
        ]

        data = {
            'leads': leads_data,
        }

        serializer = ECGModelSerializer(
            data=data,
            context={'request': self.request},
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

        # Optionally, you can test the LeadsSerializer as well
        leads_serializer = LeadsSerializer(data=leads_data, many=True)
        self.assertTrue(leads_serializer.is_valid())


class ECGResponseSerializerTests(TestCase):
    def test_ecg_response_serializer(self):
        data = {'lead_name': 'I', 'zero_crossings_count': 5}

        serializer = ECGResponseSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['lead_name'], 'I')
        self.assertEqual(serializer.validated_data['zero_crossings_count'], 5)

    def test_ecg_response_serializer_invalid_data(self):
        # Test with invalid data (missing 'zero_crossings_count')
        data = {'lead_name': 'I'}

        serializer = ECGResponseSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('zero_crossings_count', serializer.errors)

    def test_ecg_response_serializer_invalid_type(self):
        # Test with invalid data types
        data = {'lead_name': {}, 'zero_crossings_count': 'invalid'}

        serializer = ECGResponseSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('lead_name', serializer.errors)
        self.assertIn('zero_crossings_count', serializer.errors)
