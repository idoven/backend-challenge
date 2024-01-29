import json

from rest_framework import serializers
from connector.models import ECGModel, UserModel
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import re


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if (username or email) and password:
            if username:
                user = authenticate(username=username, password=password)
            elif email:
                user = authenticate(email=email, password=password)
            else:
                raise serializers.ValidationError('Invalid credentials')
            print(f'\n\n##################################\n variable: {user}\n')
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include both username/email and password')

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'

    def validate_password(self, value):
        # Check if password has at least 8 characters
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Check if password has at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        # Check if password has at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserRegistrationSerializer, self).create(validated_data)


# class LeadsModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LeadsModel
#         fields = '__all__'


class LeadsSerializer(serializers.Serializer):
    LEAD_IDENTIFIERS = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

    name = serializers.ChoiceField(choices=[(lead, lead) for lead in LEAD_IDENTIFIERS],
                                   help_text='The lead identifier of ECG leads')

    num_samples = serializers.IntegerField(required=False, help_text='The sample size of the signal')
    signal = serializers.CharField(help_text='A list of integer values')


class ECGModelSerializer(serializers.ModelSerializer):
    leads = LeadsSerializer(many=True)

    class Meta:
        model = ECGModel
        fields = '__all__'


class ECGResponseSerializer(serializers.Serializer):
    lead_name = serializers.CharField()
    zero_crossings_count = serializers.IntegerField()
