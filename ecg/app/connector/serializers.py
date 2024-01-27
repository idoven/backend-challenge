from rest_framework import serializers
from connector.models import ECGModel, LeadsModel


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
