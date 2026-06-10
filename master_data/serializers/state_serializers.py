from rest_framework import serializers

from master_data.models.state import State


class StateDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "state_name"]
        read_only_fields = fields
