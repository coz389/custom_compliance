from rest_framework import serializers

from master_data.models.country import Country
from master_data.models.seaport import Seaport
from master_data.serializers.city_serializers import CountryBasicSerializer


class SeaportSerializer(serializers.ModelSerializer):
    country = CountryBasicSerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source="country",
        write_only=True,
        required=False,
        allow_null=True,
    )
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Seaport
        fields = [
            "id",
            "status",
            "port_name",
            "unloc",
            "utc_offset",
            "latitude",
            "longitude",
            "country_id",
            "country",
            "tradelane_name",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]


class SeaportListRequestSerializer(serializers.Serializer):
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search by port name, UNLOC, country or tradelane",
    )
    port_name = serializers.CharField(required=False, allow_blank=True)
    unloc = serializers.CharField(required=False, allow_blank=True)
    country = serializers.IntegerField(required=False)
    tradelane_name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default="created_at")
    sort_order = serializers.ChoiceField(
        choices=["asc", "desc"], required=False, default="desc"
    )
