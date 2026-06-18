from rest_framework import serializers
from master_data.models import Company, Customer


class CompanySerializer(serializers.ModelSerializer):
    def validate_company_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Company name cannot be empty.")

        instance = self.instance
        query = Company.all_objects.filter(company_name__iexact=value)

        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Company metadata integrity validation failed.",
                "data": {
                    "company_name": [
                        "Company with this name already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)

        return value

    def validate_company_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Company code cannot be empty.")

        instance = self.instance
        query = Company.all_objects.filter(company_code__iexact=value)

        if instance:
            query = query.exclude(pk=instance.pk)

        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Company metadata integrity validation failed.",
                "data": {
                    "company_code": [
                        "Company with this code already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)

        return value

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer", required=False, allow_null=True,
    )
    customer_name = serializers.CharField(source="customer.customer_name", read_only=True, allow_null=True, default=None)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Company
        fields = [
            'id', 'customer_id', 'customer_name', 'company_name', 'company_code', 'status',
            'domain_name', 'contact_email', 'contact_phone',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        ]


class CompanyListRequestSerializer(serializers.Serializer):
    """Only for Swagger documentation of list endpoint filters and pagination. Not used for actual filtering logic."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by company_name, company_code or domain_name")
    company_name = serializers.CharField(required=False, allow_blank=True)
    company_code = serializers.CharField(required=False, allow_blank=True)
    customer = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
