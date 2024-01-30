import json
import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from connector.models import ECGModel, UserModel


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError(
                'Must include both username and password',
            )

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'

    def validate_password(self, value):
        # Check if password has at least 8 characters
        if len(value) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long.'
            )

        # Check if password has at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter.'
            )

        # Check if password has at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):  # noqa: E501
            raise serializers.ValidationError(
                'Password must contain at least one special character.'
            )

        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LeadsSerializer(serializers.Serializer):
    LEAD_IDENTIFIERS = [
        'I',
        'II',
        'III',
        'aVR',
        'aVL',
        'aVF',
        'V1',
        'V2',
        'V3',
        'V4',
        'V5',
        'V6',
    ]

    name = serializers.ChoiceField(
        choices=[(lead, lead) for lead in LEAD_IDENTIFIERS],
        help_text='The lead identifier of ECG leads',
    )

    num_samples = serializers.IntegerField(
        required=False, help_text='The sample size of the signal'
    )
    signal = serializers.CharField(
        help_text='A list of integer values in the format [1, 2, 3, -4, 2, -6]'
    )

    def validate_signal(self, value):
        try:
            # Try to parse the input string as
            # a JSON list of integers or floats
            parsed_data = json.loads(value)

            # Ensure the parsed data is a list of numbers (integers or floats)
            if not isinstance(parsed_data, list) or not all(
                isinstance(x, (int, float)) for x in parsed_data
            ):
                raise serializers.ValidationError(
                    'Invalid signal format. '
                    'Must be a list of numbers (integers or floats).'
                )

            return value  # Return originally received string
        except (TypeError, ValueError):
            # If parsing fails, raise a validation error
            raise serializers.ValidationError(
                'Invalid signal format.'
                ' Must be a valid JSON list'
                ' of numbers (integers or floats).'
            )


class ECGModelSerializer(serializers.ModelSerializer):
    leads = LeadsSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ECGModel
        fields = '__all__'
        read_only_fields = ('date',)


class ECGResponseSerializer(serializers.Serializer):
    lead_name = serializers.CharField()
    zero_crossings_count = serializers.IntegerField()
