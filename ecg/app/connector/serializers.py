from rest_framework import serializers
from connector.models import ECGModel, LeadsModel, UserModel
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


class LeadsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadsModel
        fields = ['name', 'num_samples', 'signal']


class ECGModelSerializer(serializers.ModelSerializer):
    leads = LeadsModelSerializer(many=True, write_only=True)

    class Meta:
        model = ECGModel
        fields = ['id', 'date', 'leads']

    def create(self, validated_data):
        leads_data = validated_data.pop('leads')
        ecg_instance = ECGModel.objects.create(**validated_data)

        for lead_data in leads_data:
            LeadsModel.objects.create(ecg=ecg_instance, **lead_data)

        return ecg_instance


class ECGResponseSerializer(serializers.Serializer):
    channel_name = serializers.CharField()
    zero_crossings_count = serializers.IntegerField()
