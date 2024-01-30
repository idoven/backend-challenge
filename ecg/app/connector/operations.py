import json

import numpy as np
from connector import serializers
from connector.models import ECGModel
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import logging
from collections import namedtuple
from django.forms.models import model_to_dict

from rest_framework import status

ErrorTuple = namedtuple('Error', ['code', 'status', 'details'])

logger = logging.getLogger(__name__)

ERROR_LIST = [
    ErrorTuple('RESOURCE_NOT_AVAILABLE', status.HTTP_404_NOT_FOUND, 'Resource not available'),
    ErrorTuple('INVALID_VALUE', status.HTTP_400_BAD_REQUEST, 'Invalid value'),
    ErrorTuple('INTERNAL_SERVER_ERROR', status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal server error')
]


class ECGOperations:
    serializer_class = serializers.ECGModelSerializer

    def _zero_crossing(self, signal):
        """
        Calculates the number of times each ECG channel crosses zero
        """
        signal = np.array(json.loads(signal))
        zero_crossing_count = ((signal[:-1] * signal[1:]) < 0).sum()

        return zero_crossing_count

    def get_zero_crossing_count(self, ecg_record):
        """
        Gets the ECG record from the database on given id
        returns number of times each ECG channel crosses zero

        ecg_id: the id of the ECG record
        """
        leads = ecg_record.leads
        response = []
        for lead in leads:
            signal = lead.get('signal')
            zero_crossing_count = self._zero_crossing(signal)

            response.append({
                'zero_crossing_count': zero_crossing_count,
                'lead_name': lead.get('name')
            })

        return response

    def get_ecg_instance(self, ecg_id):
        try:
            ecg_record = ECGModel.objects.get(pk=ecg_id)
            return ecg_record
        except ECGModel.DoesNotExist:
            error_message = 'Model/Record not found'
            logger.error(error_message)
            raise ObjectDoesNotExist(ERROR_LIST.RESOURCE_NOT_AVAILABLE, error_message)
        except ValidationError as e:
            logger.error(e.message)
            raise ValidationError(ERROR_LIST.INVALID_VALUE, e.message)
        except Exception as e:
            # log any other kind of error
            logger.error(e)
            raise Exception(ERROR_LIST.INTERNAL_SERVER_ERROR, e.__cause__)

    def create_ecg_record(self, ecg_data, context):
        """
        Creates ECG record in database

        ecg_data: ECG data
        """
        try:
            serializer = self.serializer_class(data=ecg_data, context=context)
        except ECGModel.DoesNotExist:
            error_message = 'Model/Record not found'
            logger.error(error_message)
            raise ObjectDoesNotExist(ERROR_LIST.RESOURCE_NOT_AVAILABLE, error_message)
        except ValidationError as e:
            logger.error(e.message)
            raise ValidationError(ERROR_LIST.INVALID_VALUE, e.message)
        except Exception as e:
            # log any other kind of error
            logger.error(e)
            raise Exception(ERROR_LIST.INTERNAL_SERVER_ERROR, e.__cause__)

        serializer.is_valid(raise_exception=True)
        serializer.save()
