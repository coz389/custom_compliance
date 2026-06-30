from rest_framework import serializers

from master_data.models import CustomerLspAssoc


class CustomerLspAssocSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
    carrier_name = serializers.CharField(source='carrier.carrier_name', read_only=True)
    transport_name = serializers.CharField(source='transport.name', read_only=True, allow_null=True, default=None)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = CustomerLspAssoc
        fields = [
            'id', 'status', 'customer', 'customer_name',
            'carrier', 'carrier_name',
            'transport', 'transport_name', 'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class CustomerLspAssocListSerializer(serializers.Serializer):
    customer = serializers.IntegerField(required=False)
    carrier = serializers.IntegerField(required=False)
    transport = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False, allow_null=True)
    search = serializers.CharField(required=False)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.CharField(required=False, default='desc')
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
