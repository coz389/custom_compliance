from rest_framework import serializers

from master_data.models.transport_mode import TransportMode


class TransportModeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ["id", "code", "name"]
        read_only_fields = fields


