"""
Serializers for the electrocardiograms API View
"""
from rest_framework import serializers
from core.models import Electrocardiogram, Lead


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for the lead object."""

    class Meta:
        model = Lead
        fields = ['name', 'samples', 'signal']
        extra_kwargs = {'samples': {'required': False}}


class ElectrocardiogramSerializer(serializers.ModelSerializer):
    """Serializer for the electrocardiogram object."""

    leads = LeadSerializer(many=True)

    signal_zeros = serializers.SerializerMethodField('get_signal_zeros')

    def get_signal_zeros(self, obj):
        """
        Get number of times the signal reaches zero value
        """
        signal = list(obj.leads.all().values("signal"))
        signal_zeros = sum([v['signal'].count(0) for v in signal])
        return signal_zeros

    class Meta:
        model = Electrocardiogram
        fields = ['id', 'leads', 'signal_zeros']
        read_only = ['id']

    def create(self, validated_data):
        """
        Create method for use in post endpoint for ecg
        """
        lead_data = validated_data.pop("leads")
        electrocardiogram = Electrocardiogram.objects.create(**validated_data)
        for lead in lead_data:
            Lead.objects.create(electrocardiogram=electrocardiogram, **lead)
        return electrocardiogram
