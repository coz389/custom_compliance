from rest_framework import serializers

from master_data.models import CustomerContact


class CustomerContactSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    country_name = serializers.CharField(source='country.country_name', read_only=True, allow_null=True, default=None)
    port_name = serializers.CharField(source='port.port_name', read_only=True, allow_null=True, default=None)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = CustomerContact
        fields = [
            'id', 'customer', 'customer_name', 'transport_mode', 'service_type',
            'country', 'country_name', 'port', 'port_name',
            'email', 'phone_number', 'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class CustomerContactListSerializer(serializers.Serializer):
    customer = serializers.IntegerField(required=False)
    country = serializers.IntegerField(required=False)
    port = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False)
    sort_column = serializers.CharField(required=False, default='updated_at')
    sort_order = serializers.CharField(required=False, default='desc')
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
