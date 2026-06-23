from rest_framework import serializers

from master_data.models import Country, State, Equipment, Customer, TransportMode


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

class CustomerCompanyDropdownSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ["id", "customer_name", "customer_code", "companies"]
        read_only_fields = fields

    def get_companies(self, obj):
        return obj.company_set.values("id", "company_name", "company_code")


class TransportModeDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ["id", "code", "name"]
        read_only_fields = fields