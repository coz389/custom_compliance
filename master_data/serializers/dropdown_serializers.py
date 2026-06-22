from rest_framework import serializers

from master_data.models.country import Country
from master_data.models.customer import Customer
from master_data.models.equipment import Equipment
from master_data.models.state import State
from master_data.models.transport_mode import TransportMode


class CountryDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "country_name",
            "iso3",
            "iso2",
            "phonecode",
            "capital",
            "currency",
            "currency_name",
            "currency_symbol",
            "region",
            "nationality",
            "timezones",
            "latitude",
            "longitude",
        ]
        read_only_fields = fields


class StateDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "state_name"]
        read_only_fields = fields


class EquipmentDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ["id", "code", "type", "description"]
        read_only_fields = fields


class CustomerDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "customer_name", "customer_code"]
        read_only_fields = fields


class TransportModeDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ["id", "code", "name"]
        read_only_fields = fields