from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import User, Role, Module, RolePermission, user
from rest_framework.validators import UniqueValidator




User = get_user_model()
class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields


class RoleSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Role name cannot be empty.")
        
        instance = self.instance 
        
        # Puraane code constraint ke mutabik query execute karna (bina soft-delete check ke)
        # Kyunki database level par unique=True hai, isliye hum pure table mein look up karenge
        query = Role.all_objects.filter(name__iexact=value)
        
        if instance:
            query = query.exclude(pk=instance.pk)
            
        if query.exists():
            # DRF standard structural format ko bypass karke custom response pattern construct karna
            custom_error_payload = {
                "success": False,
                "message": "Role metadata integrity validation failed.",
                "data": {
                    "name": [
                        "role with this name already exists."
                    ]
                }
            }
            raise serializers.ValidationError(custom_error_payload)
        
        return value
    
    # Nested user data (read-only)
    # created_by = UserBasicSerializer(read_only=True)
    # updated_by = UserBasicSerializer(read_only=True)
    # deleted_by = UserBasicSerializer(read_only=True)
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Role
        # fields = '__all__'
        fields = ['id', 'name', 'code', 'description', 'status', 'created_at','created_by', 'updated_by', 'updated_at' ,'deleted_by']
        read_only_fields = ['created_by', 'updated_by', 'deleted_by']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return getattr(obj.created_by, 'name', obj.created_by.username)
        return None
    
    def create(self, validated_data):
        raw_name = validated_data.get('name')
        clean_spaces = " ".join(raw_name.split())
        generated_code = clean_spaces.replace(' ', '_').lower()
        # CRITICAL VALIDATION DETECTOR: 80 characters length boundary checkpoint
        if len(generated_code) > 80:
            raise serializers.ValidationError({
                "success": False,
                "message": "The generated configuration identifier is too long.",
                "data": {
                    "name": [
                        f"The name provided generates a code '{generated_code}' ({len(generated_code)} characters) which exceeds the system maximum length threshold of 80 characters."
                    ]
                }
            })
        # Database Level Integrity Guard (Unique Constraint Check)
        if Role.objects.filter(code=generated_code).exists():
            raise serializers.ValidationError({
                "code": f"The generated code '{generated_code}' already exists in the system."
            })

        # Inject generated code into validated data mapping
        validated_data['code'] = generated_code
        return super().create(validated_data)
        
class RoleListRequestSerializer(serializers.Serializer):
    """ Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Name, code ya description mein search karein")
    name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')