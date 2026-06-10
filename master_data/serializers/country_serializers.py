from rest_framework import serializers

from master_data.models.country import Country


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
