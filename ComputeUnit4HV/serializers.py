from rest_framework import serializers
from .models.switch import PrivateSwitch, InternalSwitch, ExternalSwitch


class PrivateSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateSwitch
        fields = '__all__'


class InternalSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalSwitch
        fields = '__all__'


class ExternalSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSwitch
        fields = '__all__'
