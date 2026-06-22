from rest_framework import serializers

from master_data.models.transport_mode import TransportMode


class TransportModeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ["id", "code", "name"]
        read_only_fields = fields


class TransportModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportMode
        fields = ['id', 'code', 'name', 'status', 'created_at']


class TransportModeListRequestSerializer(serializers.Serializer):
    """Only for Swagger documentation of list endpoint filters and pagination. Not used for actual filtering logic."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by code or name")
    code = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='desc')
