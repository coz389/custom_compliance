from rest_framework import serializers

from master_data.models import EmailTemplate


class EmailTemplateListSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    message_body = serializers.CharField(source='message')
    customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
    status_name = serializers.CharField(source='status_ref.name', read_only=True)
    template_type_name = serializers.CharField(source='template_type.title', read_only=True)

    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'status', 'customer', 'customer_name',
            'status_ref', 'status_name', 'template_type', 'template_type_name',
            'template_title', 'email_to', 'email_cc',
            'email_bcc', 'subject', 'message_body', 'signature', 'signature_logo',
            'has_attachment', 'created_by', 'created_at', 'updated_by', 'updated_at',
        ]


class EmailTemplateListRequestSerializer(serializers.Serializer):
    """
    Only for documentation and validation of list endpoint filters and pagination
    parameters in Swagger. Not used for actual filtering logic in the view.
    """
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search by template title or subject")
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    company_id = serializers.IntegerField(required=False, allow_null=True)
    status_id = serializers.IntegerField(required=False, allow_null=True)
    template_type = serializers.IntegerField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='desc')


class EmailTemplateCreateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(source='message')
    class Meta:
        model = EmailTemplate
        fields = [
            'status', 'customer', 'status_ref', 'template_type',
            'template_title', 'email_to', 'email_cc', 'email_bcc', 'subject',
            'message_body', 'signature', 'signature_logo', 'has_attachment',
        ]

    def validate_template_title(self, value):
        return value.strip()


class EmailTemplateUpdateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(source='message')
    class Meta:
        model = EmailTemplate
        fields = [
            'status', 'customer', 'status_ref', 'template_type',
            'template_title', 'email_to', 'email_cc', 'email_bcc', 'subject',
            'message_body', 'signature', 'signature_logo', 'has_attachment',
        ]
