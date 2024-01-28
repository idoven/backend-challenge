from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class UserModel(AbstractUser):
    # Restrict username to alphanumeric characters, underscores or hyphens
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message='Username must contain only alphanumeric characters.',
    )

    is_admin = models.BooleanField(default=False)
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        help_text='unique identifier of the user')
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50,   blank=True, null=True,)
    email = models.EmailField(unique=True)


class ECGModel(models.Model):
    id = models.AutoField(primary_key=True, help_text='A unique identifier for each ECG')
    date = models.DateTimeField(auto_now_add=True, help_text='The date of creation')
    leads = models.JSONField(help_text='List of leads')

    username = models.CharField(max_length=20, help_text='user that has uploaded the ECG')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                             help_text='user that has uploaded the ECG')  # ForeignKey relationship with User model

    def __str__(self):
        return f"ECG {self.id}"


class LeadsModel(models.Model):
    ecg = models.ForeignKey(ECGModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text='The lead identifier')
    num_samples = models.IntegerField(null=True, blank=True, help_text='The sample size of the signal')
    signal = models.JSONField(help_text='A list of integer values')

    def __str__(self):
        return f"{self.ecg} - Lead {self.name}"
