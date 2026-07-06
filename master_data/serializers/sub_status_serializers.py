from rest_framework import serializers
from django.contrib.auth import get_user_model
from master_data.models import SubStatus


User = get_user_model()


class SubStatusUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=False)

    class Meta:
        model = SubStatus
        fields = ['id', 'name', 'description', 'status']


class SubStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = SubStatus
        fields = [
            'id', 'name', 'description',
            'status', 'created_by', 'created_at', 'updated_by', 'updated_at'
        ]

    def get_created_by_name(self, obj):
        if obj.created_by:
            return getattr(obj.created_by, 'name', obj.created_by.username)
        return None

    def create(self, validated_data):
        return super().create(validated_data)


class SubStatusListRequestSerializer(serializers.Serializer):
    """ Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search only Name and Description")
    name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='id')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
