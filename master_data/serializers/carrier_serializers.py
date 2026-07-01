from rest_framework import serializers

from master_data.models import Carrier
from master_data.models.transport_mode import TransportMode


class CarrierSerializer(serializers.ModelSerializer):
    def validate_carrier_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Carrier name cannot be empty.")

        instance = self.instance
        query = Carrier.all_objects.filter(carrier_name__iexact=value)

        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Carrier metadata integrity validation failed.",
                "data": {
                    "carrier_name": [
                        "Carrier with this name already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)

        return value

    transport_id = serializers.PrimaryKeyRelatedField(
        queryset=TransportMode.objects.all(), source="transport", required=False, allow_null=True,
    )
    transport_name = serializers.CharField(source="transport.name", read_only=True, allow_null=True, default=None)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Carrier
        fields = [
            'id', 'type', 'carrier_name', 'carrier_scac', 'web_link',
            'transport_id', 'transport_name', 'logo', 'status',
            'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class CarrierListRequestSerializer(serializers.Serializer):
    """Only for Swagger documentation of list endpoint filters and pagination. Not used for actual filtering logic."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by carrier_name, carrier_scac or type")
    carrier_name = serializers.CharField(required=False, allow_blank=True)
    carrier_scac = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False, allow_blank=True)
    transport = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='desc')
