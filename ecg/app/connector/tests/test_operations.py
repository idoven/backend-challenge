from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.exceptions import APIException, NotFound

from connector.models import ECGModel
from connector.operations import ECGOperations


class ECGOperationsTests(TestCase):
    def setUp(self):
        self.ecg_operations = ECGOperations()
        self.ecg_data = {
            'leads': [
                {
                    'name': 'I',
                    'num_samples': 0,
                    'signal': '[1,2,3,-4,2,-6]',
                }
            ]
        }
        self.context = {'request': MagicMock()}

    @patch('connector.serializers.ECGModelSerializer')
    def test_create_ecg_record(self, mock_ecg_model_serializer):
        # Mocking the serializer instance
        serializer_instance = mock_ecg_model_serializer.return_value
        serializer_instance.is_valid.return_value = True
        serializer_instance.save.return_value = MagicMock()

        # Mocking the create_ecg_record method
        with patch(
            'connector.operations.ECGOperations.serializer_class',
            mock_ecg_model_serializer,
        ):
            self.ecg_operations.create_ecg_record(ecg_data={}, context={})

        # Assert that the serializer's is_valid and save methods are called
        serializer_instance.is_valid.assert_called_once()
        serializer_instance.save.assert_called_once()

    @patch('connector.operations.ECGModel.objects.get')
    def test_get_ecg_instance(self, mock_get_ecg_model):
        # Mocking the ECGModel.objects.get method
        mock_ecg_instance = MagicMock(spec=ECGModel)
        mock_get_ecg_model.return_value = mock_ecg_instance

        # Call the get_ecg_instance method
        result = self.ecg_operations.get_ecg_instance(ecg_id=1)

        # Assert that the mocked method is
        # called and returns the expected instance
        mock_get_ecg_model.assert_called_once_with(pk=1)
        self.assertEqual(result, mock_ecg_instance)

    @patch('connector.operations.ECGModel.objects.get')
    def test_get_ecg_instance_not_found(self, mock_get_ecg_model):
        # Mocking the ECGModel.objects.get
        # method to raise a DoesNotExist exception
        mock_get_ecg_model.side_effect = ECGModel.DoesNotExist()

        # Call the get_ecg_instance method
        with self.assertRaises(NotFound) as context:
            self.ecg_operations.get_ecg_instance(ecg_id=1)

        # Assert that the exception detail
        # contains the original DoesNotExist exception
        self.assertIsInstance(context.exception, NotFound)

    @patch('connector.operations.ECGModel.objects.get')
    def test_get_ecg_instance_validation_error(self, mock_get_ecg_model):
        # Mocking the ECGModel.objects.get
        # method to raise a Django ValidationError
        mock_get_ecg_model.side_effect = ValidationError('Invalid Value')

        # Call the get_ecg_instance method
        with self.assertRaises(ValidationError) as context:
            self.ecg_operations.get_ecg_instance(ecg_id=1)

        self.assertEqual(context.exception.message, 'Invalid Value')

    @patch('connector.operations.ECGModel.objects.get')
    def test_get_ecg_instance_api_exception(self, mock_get_ecg_model):
        # Mocking the ECGModel.objects.get method to raise an APIException
        mock_get_ecg_model.side_effect = APIException('API exception')

        # Call the get_ecg_instance method
        with self.assertRaises(APIException) as context:
            self.ecg_operations.get_ecg_instance(ecg_id=1)

        # Assert that the exception detail contains the original APIException
        self.assertEqual(str(context.exception), 'API exception')

    def test_zero_crossing(self):
        data = '[1, 2, 3, -4, 2, -6]'

        # Call the _zero_crossing method
        result = self.ecg_operations._zero_crossing(signal=data)

        self.assertEqual(result, 3)

    def test_get_zero_crossing_count(self):
        # Mocking an ECGModel instance with leads
        ecg_instance = MagicMock(spec=ECGModel)
        ecg_instance.leads = [
            {'name': 'I', 'signal': '[1, 2, 3, -4, 2, -6]'},
            {'name': 'II', 'signal': '[3, 2, 1, -1, -2, -3]'},
        ]

        # Mocking the _zero_crossing method
        with patch.object(
            self.ecg_operations, '_zero_crossing', side_effect=[3, 4]
        ):
            # Call the get_zero_crossing_count method
            result = self.ecg_operations.get_zero_crossing_count(ecg_instance)

            # Assert that the mocked method is
            # called and returns the expected result
            self.assertEqual(
                result,
                [
                    {'zero_crossing_count': 3, 'lead_name': 'I'},
                    {'zero_crossing_count': 4, 'lead_name': 'II'},
                ],
            )
