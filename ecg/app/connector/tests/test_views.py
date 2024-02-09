from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.test import APIClient

from connector.models import UserModel


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.login_url = '/api/login/'

    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = '/api/registration/'
        self.registration_data = {
            'username': 'newuser',
            'password': 'Password12!',
            'first_name': 'name',
            'last_name': 'last_name',
            'email': 'email@email.com',
        }

    def test_user_registration(self):
        response = self.client.post(
            self.registration_url,
            self.registration_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)

    def test_user_registration_fail(self):
        data = {'username': 'username', 'password': 'password'}
        response = self.client.post(self.registration_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ECGViewTest(TestCase):
    URL_NAME_ECG = 'ecg_monitoring'

    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='Testpassword1!',
            first_name='name',
            last_name='lastname',
            email='email@email.com',
        )
        self.user_2 = UserModel.objects.create_user(
            username='testuser2',
            password='Testpassword2!',
            first_name='name',
            last_name='lastname',
            email='email2@email.com',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.ecg_url_get = self.api_url(self.URL_NAME_ECG, ['1'])
        self.ecg_url_not_exist = self.api_url(self.URL_NAME_ECG, ['1345'])

        self.ecg_data = {
            'leads': [
                {'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4,2,-6]'},
            ]
        }

    def tearDown(self):
        # Clean up created users and tokens
        UserModel.objects.all().delete()
        Token.objects.all().delete()

    class ECGInstance:
        leads = [{'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4,2,-6]'}]

        def __init__(self, user):
            self.user = user

    @classmethod
    def api_url(cls, view_name, args=None):
        url = reverse(view_name, args=args)
        return url

    @patch('connector.views.ECGOperations', autospec=True)
    def test_create_ecg_record(self, mock_create_ecg_record):
        response = self.client.post(
            reverse(self.URL_NAME_ECG),
            data=self.ecg_data,
            format='json',
        )

        mock_create_ecg_record.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'ECG record created successfully')

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    def test_retrieve_zero_crossing(self, mock_get_ecg_instance):
        # Mock the get_ecg_instance function to return a mock ECG instance
        mock_ecg_instance = self.ECGInstance(user=self.user)
        mock_get_ecg_instance.return_value = mock_ecg_instance

        response = self.client.get(self.ecg_url_get)
        # Assert that the mock function was called
        # and the response status code is OK
        mock_get_ecg_instance.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    def test_retrieve_zero_crossing_fail(self, mock_get_ecg_instance):
        """
        Should return  PERMISSION DENIED when user is trying
        to access ecg data that they haven't created
        """
        # Mock the get_ecg_instance function to return a mock ECG instance
        mock_ecg_instance = self.ECGInstance(user=self.user_2)
        mock_get_ecg_instance.return_value = mock_ecg_instance

        response = self.client.get(self.ecg_url_get)
        # Assert that the mock function was called
        # and the response status code is OK
        mock_get_ecg_instance.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    @patch('connector.operations.ECGOperations.update_ecg_record')
    def test_update_ecg_success(
        self, mock_update_ecg_record, mock_get_ecg_instance
    ):
        # Mock the get_ecg_instance method to return a mock ECG instance
        mock_ecg_instance = self.ECGInstance(user=self.user)
        mock_get_ecg_instance.return_value = mock_ecg_instance

        # Mock the update_ecg_record method
        mock_update_ecg_record.return_value = None

        data = {
            'id': 1,
            'leads': [
                {'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4]'},
            ],
        }

        response = self.client.put(
            reverse(self.URL_NAME_ECG),
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_get_ecg_instance.assert_called_once()

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    def test_update_ecg_permission_denied(self, mock_get_ecg_instance):
        # Mock the get_ecg_instance method to return a mock ECG instance
        mock_ecg_instance = self.ECGInstance(user=self.user_2)
        mock_get_ecg_instance.return_value = mock_ecg_instance

        data = {
            'id': 1,
            'leads': [
                {'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4]'},
            ],
        }

        response = self.client.put(
            reverse(self.URL_NAME_ECG),
            data=data,
            format='json',
        )
        # Assert that the status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    def test_update_ecg_not_found(self, mock_get_ecg_instance):
        # Mock the get_ecg_instance method to raise a NotFound exception
        mock_get_ecg_instance.side_effect = NotFound

        data = {
            'id': 2,
            'leads': [
                {'name': 'I', 'num_samples': 0, 'signal': '[1,2,3,-4]'},
            ],
        }

        response = self.client.put(
            reverse(self.URL_NAME_ECG),
            data=data,
            format='json',
        )
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    def test_retrieve_ecg_success(self, mock_get_ecg_instance):
        # Mock the get_ecg_instance method to return a mock ECG instance
        mock_ecg_instance = self.ECGInstance(user=self.user)
        mock_get_ecg_instance.return_value = mock_ecg_instance

        ecg_id = '1'

        response = self.client.get(
            self.ecg_url_get,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get_ecg_instance.assert_called_once_with(ecg_id)

    @patch('connector.operations.ECGOperations.get_ecg_instance')
    @patch('connector.operations.ECGOperations.delete_ecg_record')
    def test_delete_ecg_success(
        self, mock_delete_ecg_record, mock_get_ecg_instance
    ):
        # Mock the get_ecg_instance method to return a mock ECG instance
        ecg_instance_mock = mock_get_ecg_instance.return_value

        response = self.client.delete(self.ecg_url_get)

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the delete_ecg_record
        # method was called with the correct arguments
        mock_delete_ecg_record.assert_called_once_with(ecg_instance_mock)
