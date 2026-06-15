from rest_framework import serializers

from master_data.models.container import Container
from master_data.serializers.transport_mode_serializers import (
    TransportModeBasicSerializer,
)


class ContainerSerializer(serializers.ModelSerializer):
    transport = TransportModeBasicSerializer(read_only=True)
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True, allow_null=True,)
    updated_by = serializers.SlugRelatedField(slug_field="username", read_only=True, allow_null=True,)

    class Meta:
        model = Container
        fields = [
            "id",
            "status",
            "transport_id",
            "transport",
            "code",
            "iso",
            "net_weight",
            "net_volume",
            "size",
            "type",
            "description",
            "dimension",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]


class ContainerListRequestSerializer(serializers.Serializer):
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search by code, iso, size, type, description or dimension",
    )
    transport_id = serializers.IntegerField(required=False)
    code = serializers.CharField(required=False, allow_blank=True)
    iso = serializers.CharField(required=False, allow_blank=True)
    size = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    dimension = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default="created_at")
    sort_order = serializers.ChoiceField(
        choices=["asc", "desc"], required=False, default="desc"
    )
