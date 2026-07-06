from rest_framework import serializers
from master_data.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='name', required=False, allow_blank=False)
    customer_code = serializers.CharField(source='code', required=False, allow_blank=False)

    def validate_customer_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Customer name cannot be empty.")

        instance = self.instance
        query = Customer.all_objects.filter(name__iexact=value)

        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Customer metadata integrity validation failed.",
                "data": {
                    "customer_name": [
                        "Customer with this name already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)

        return value

    def validate_customer_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Customer code cannot be empty.")

        instance = self.instance
        query = Customer.all_objects.filter(code__iexact=value)

        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Customer metadata integrity validation failed.",
                "data": {
                    "customer_code": [
                        "Customer with this code already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)

        return value

    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_name', 'customer_code', 'status',
            'domain_name', 'contact_email', 'contact_phone',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        ]


class CustomerListRequestSerializer(serializers.Serializer):
    """Only for Swagger documentation of list endpoint filters and pagination. Not used for actual filtering logic."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by customer_name, customer_code, domain_name or contact_email")
    customer_name = serializers.CharField(required=False, allow_blank=True)
    customer_code = serializers.CharField(required=False, allow_blank=True)
    domain_name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
