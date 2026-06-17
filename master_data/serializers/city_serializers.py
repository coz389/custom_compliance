from rest_framework import serializers
from master_data.models.city import City
from master_data.models.state import State
from master_data.models.country import Country


class CountryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "country_name"]
        read_only_fields = fields


class StateBasicSerializer(serializers.ModelSerializer):
    country = CountryBasicSerializer(read_only=True)

    class Meta:
        model = State
        fields = ["id", "state_name", "country", "country_code"]
        read_only_fields = fields


class CitySerializer(serializers.ModelSerializer):
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        source="state",
        required=False,
        allow_null=True,
    )
    state_name = serializers.CharField(source="state.state_name", read_only=True, allow_null=True, default=None)

    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source="country",
        required=False,
        allow_null=True,
    )
    country_name = serializers.CharField(source="country.country_name", read_only=True, allow_null=True, default=None)

    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = City
        fields = [
            "id",
            "city_name",
            "state_id",
            "state_name",
            "country_id",
            "country_name",
            "latitude",
            "longitude",
            "unloc",
            "utc_offset",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]

    def validate(self, attrs):
        state = attrs.get("state")
        country = attrs.get("country")

        if state and country and state.country_id != country.id:
            raise serializers.ValidationError(
                "The selected state does not belong to the selected country."
            )

        return attrs


class CityListRequestSerializer(serializers.Serializer):
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search by city name, state, country or UNLOC",
    )

    city_name = serializers.CharField(required=False, allow_blank=True)
    state = serializers.IntegerField(required=False)
    country = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default="created_at")
    sort_order = serializers.ChoiceField(
        choices=["asc", "desc"], required=False, default="desc"
    )
