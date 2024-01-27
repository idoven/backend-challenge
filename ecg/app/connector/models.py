from django.db import models


class ECGModel(models.Model):
    id = models.AutoField(primary_key=True, help_text='A unique identifier for each ECG')
    date = models.DateTimeField(auto_now_add=True, help_text='The date of creation')
    leads = models.JSONField(help_text='List of leads')

    def __str__(self):
        return f"ECG {self.id}"


class LeadsModel(models.Model):
    ecg = models.ForeignKey(ECGModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text='The lead identifier')
    num_samples = models.IntegerField(null=True, blank=True, help_text='The sample size of the signal')
    signal = models.JSONField(help_text='A list of integer values')

    def __str__(self):
        return f"{self.ecg} - Lead {self.name}"
