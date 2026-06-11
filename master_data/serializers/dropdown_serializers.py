from rest_framework import serializers

from master_data.models.country import Country
from master_data.models.state import State


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
