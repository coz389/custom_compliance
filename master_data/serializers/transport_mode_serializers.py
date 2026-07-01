from rest_framework import serializers

from master_data.models.transport_mode import TransportMode


class TransportModeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ["id", "code", "name"]
        read_only_fields = fields


class TransportModeSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = TransportMode
        fields = ['id', 'code', 'name', 'status', 'created_at', 'created_by']


class TransportModeListRequestSerializer(serializers.Serializer):
    """Only for Swagger documentation of list endpoint filters and pagination. Not used for actual filtering logic."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by code or name")
    code = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_by = serializers.CharField(required=False, allow_blank=True, help_text="Filter by username")
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='desc')
