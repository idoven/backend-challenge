import json
import logging

import numpy as np
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound

from connector import serializers
from connector.models import ECGModel

logger = logging.getLogger(__name__)


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Validation error'


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

            response.append(
                {
                    'zero_crossing_count': zero_crossing_count,
                    'lead_name': lead.get('name'),
                }
            )

        return response

    def get_ecg_instance(self, ecg_id):
        try:
            ecg_record = ECGModel.objects.get(pk=ecg_id)
            return ecg_record
        except ECGModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)


def create_ecg_record(self, ecg_data, context):
    """
    Creates ECG record in database

    ecg_data: ECG data
    """
    try:
        serializer = self.serializer_class(data=ecg_data, context=context)
    except ECGModel.DoesNotExist as e:
        raise NotFound(e)
    except ValidationError as e:
        raise ValidationError(e)
    except APIException as e:
        raise APIException(e)

    serializer.is_valid(raise_exception=True)
    serializer.save()
