from rest_framework import serializers

from master_data.models import CustomerDocAssoc
from master_data.serializers.customer_serializers import CustomerSerializer
from master_data.serializers.document_type_serializers import DocumentTypeSerializer
from master_data.serializers.dropdown_serializers import CountryDropdownSerializer


class CustomerDocAssocSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    export_country_name = serializers.CharField(source='export_country.country_name', read_only=True)
    import_country_name = serializers.CharField(source='import_country.country_name', read_only=True)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = CustomerDocAssoc
        fields = [
            'id', 'customer', 'customer_name', 'document_type', 'document_type_name',
            'export_country', 'export_country_name', 'import_country', 'import_country_name',
            'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class CustomerDocAssocListSerializer(serializers.Serializer):
    customer = serializers.IntegerField(required=False)
    document_type = serializers.IntegerField(required=False)
    export_country = serializers.IntegerField(required=False)
    import_country = serializers.IntegerField(required=False)
    search = serializers.CharField(required=False)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.CharField(required=False, default='desc')
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
