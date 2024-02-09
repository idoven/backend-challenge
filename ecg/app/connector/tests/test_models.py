import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from connector.models import ECGModel


class UserModelTest(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'name',
            'last_name': 'last_name',
            'email': 'testuser@example.com',
        }

    def test_create_user(self):
        user = get_user_model().objects.create_user(**self.valid_user_data)
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(user.first_name, self.valid_user_data['first_name'])
        self.assertEqual(user.last_name, self.valid_user_data['last_name'])
        self.assertEqual(user.email, self.valid_user_data['email'])
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            **self.valid_user_data, is_admin=True
        )
        self.assertTrue(superuser.is_admin)

    def test_username_validation(self):
        # Test username validation
        invalid_user_data = {
            'username': 'user with spaces',
            'password': 'testpassword',
            'first_name': 'name',
            'last_name': 'lastname',
            'email': 'testuser@example.com',
        }

        invalid_user = get_user_model()(**invalid_user_data)

        with self.assertRaisesMessage(
            ValidationError,
            'Username must contain only alphanumeric characters.',
        ):
            invalid_user.full_clean()
        # Ensure that the user is not saved to the database
        self.assertFalse(
            get_user_model()
            .objects.filter(username=invalid_user_data['username'])
            .exists()
        )

        valid_user = get_user_model()(**self.valid_user_data)
        valid_user.save()

        # Check that the user is saved successfully
        self.assertTrue(
            get_user_model()
            .objects.filter(username=self.valid_user_data['username'])
            .exists()
        )

    def test_email_uniqueness(self):
        # Test email uniqueness validation
        user1 = get_user_model().objects.create_user(  # noqa E501
            **self.valid_user_data
        )
        duplicate_user_data = {
            'username': 'anotheruser',
            'password': 'anotherpassword',
            'first_name': 'name',
            'last_name': 'last_name',
            'email': self.valid_user_data['email'],  # Reusing the same email
        }

        # Catch the IntegrityError and
        # check if it's related to the unique constraint
        with self.assertRaises(IntegrityError) as context:
            get_user_model().objects.create_user(**duplicate_user_data)

        # Check if the IntegrityError is related to
        # the unique constraint violation
        self.assertIn(
            'UNIQUE constraint failed: connector_usermodel.email',
            str(context.exception),
        )


class ECGModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )

        self.valid_ecg_data = {
            'leads': [
                {
                    'name': 'I',
                    'num_samples': 0,
                    'signal': '[1,2,3,-4,2,-6]',
                }
            ],
            'user': self.user,
        }

    def test_create_valid_ecg(self):
        # Test creating a valid ECG
        ecg = ECGModel.objects.create(**self.valid_ecg_data)

        # Check that the ECG is created successfully
        self.assertIsNotNone(ecg.id)
        self.assertIsInstance(ecg.date, datetime.datetime)
        self.assertEqual(ecg.user, self.user)
        self.assertEqual(str(ecg), f'ECG {ecg.id}')

    def test_create_invalid_ecg_missing_leads(self):
        # Test creating an ECG with missing 'leads' field
        invalid_ecg_data = self.valid_ecg_data.copy()
        invalid_ecg_data['leads'] = None

        # Catch the IntegrityError and
        # check if it's related to the unique constraint
        with self.assertRaises(IntegrityError) as context:
            ECGModel.objects.create(**invalid_ecg_data)

        # Check if the IntegrityError is
        # related to the unique constraint violation
        self.assertIn(
            'NOT NULL constraint failed: connector_ecgmodel.leads',
            str(context.exception),
        )

    def test_create_invalid_ecg_invalid_user(self):
        # Test creating an ECG with an invalid 'user' field
        invalid_ecg_data = self.valid_ecg_data.copy()
        invalid_ecg_data['user'] = 999  # Assuming there is no user with ID 999

        # Try to create the ECG and expect a ValueError
        with self.assertRaises(ValueError) as context:
            ECGModel.objects.create(**invalid_ecg_data)

        # Check if the ValueError is related to the UserModel instance
        message = (
            'Cannot assign "999": '
            '"ECGModel.user" must be a "UserModel" instance'
        )
        self.assertIn(
            message,
            str(context.exception),
        )
