from rest_framework import serializers

from master_data.models import CarrierContact


class CarrierContactSerializer(serializers.ModelSerializer):
    carrier_name = serializers.CharField(source='carrier.carrier_name', read_only=True)
    transport_name = serializers.CharField(source='transport.name', read_only=True, allow_null=True, default=None)
    primary_transport_name = serializers.CharField(source='primary_transport.name', read_only=True, allow_null=True, default=None)
    customer_name = serializers.CharField(source='customer.name', read_only=True, allow_null=True, default=None)
    country_name = serializers.CharField(source='country.country_name', read_only=True, allow_null=True, default=None)
    export_country_name = serializers.CharField(source='export_country.country_name', read_only=True, allow_null=True, default=None)
    import_country_name = serializers.CharField(source='import_country.country_name', read_only=True, allow_null=True, default=None)
    city_name = serializers.CharField(source='city.city_name', read_only=True, allow_null=True, default=None)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = CarrierContact
        fields = [
            'id', 'status',
            'carrier', 'carrier_name',
            'type',
            'transport', 'transport_name',
            'shipment_type',
            'primary_transport', 'primary_transport_name',
            'customer', 'customer_name',
            'country', 'country_name',
            'emails',
            'export_country', 'export_country_name',
            'import_country', 'import_country_name',
            'city', 'city_name',
            'service_type', 'threshold', 'auto_approve',
            'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class CarrierContactListSerializer(serializers.Serializer):
    carrier = serializers.IntegerField(required=False)
    transport = serializers.IntegerField(required=False)
    primary_transport = serializers.IntegerField(required=False)
    customer = serializers.IntegerField(required=False)
    country = serializers.IntegerField(required=False)
    export_country = serializers.IntegerField(required=False)
    import_country = serializers.IntegerField(required=False)
    city = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False, allow_null=True)
    auto_approve = serializers.BooleanField(required=False, allow_null=True)
    search = serializers.CharField(required=False)
    sort_column = serializers.CharField(required=False, default='updated_at')
    sort_order = serializers.CharField(required=False, default='desc')
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
