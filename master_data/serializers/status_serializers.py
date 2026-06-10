from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import User
from master_data.models import Status
from rest_framework.validators import UniqueValidator




User = get_user_model()
class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields


class StatusSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Status name cannot be empty.")
        
        instance = self.instance 
        query = Status.all_objects.filter(name__iexact=value)
        
        if instance:
            query = query.exclude(pk=instance.pk)
            
        if query.exists():
            custom_error_payload = {
                "success": False,
                "message": "Status metadata integrity validation failed.",
                "data": {
                    "name": [
                        "status with this name already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)
        
        return value
    
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)


    class Meta:
        model = Status
        # fields = '__all__'
        fields = ['id', 'name', 'description', 'status','created_by','created_at', 'updated_by', 'updated_at']
    def get_created_by_name(self, obj):
        if obj.created_by:
            return getattr(obj.created_by, 'name', obj.created_by.username)
        return None
    
    def create(self, validated_data):
        return super().create(validated_data)
        
class StatusListRequestSerializer(serializers.Serializer):
    """ Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search only Name and Description")
    name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')