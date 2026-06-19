from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import User, Role, Module, RolePermission, Action
from django.core.validators import RegexValidator
import re
from django.core.validators import validate_email


User = get_user_model()

class ActionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'name', 'code']
        read_only_fields = fields

class ModuleBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'code']
        read_only_fields = fields

class RolePermissionSerializer(serializers.ModelSerializer):
    module = ModuleBasicSerializer(read_only=True)
    action = ActionBasicSerializer(read_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'module', 'action']
        read_only_fields = fields

    def to_representation(self, instance):
        """
        Output JSON ko manually restructured  for better clarity in response.
        """
        # Original id ko fetch 
        data = super().to_representation(instance)
        
        # make a new custom 'module' dictionary with required fields from both module and action
        custom_module_data = {
            "id": instance.module.id,
            "module_name": instance.module.name,
            "module_code": instance.module.code,
            "action_name": instance.action.name,
            "action_code": instance.action.code
        }
        #print("Custom module data being returned:", custom_module_data)  # Debug print statement
        # Final structured response return
        return {
            "id": data['id'],
            "module": custom_module_data
        }

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    customers = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'profile_pic',
                  'bio', 'role', 'role_name', 'role_code', 'is_active', 'created_at','customers')
        read_only_fields = ('id', 'created_at')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep
    
    def get_customers(self, obj):
        grouped = {}
        for assoc in obj.user_company_assoc.all():
            company = assoc.company
            customer = company.customer
            entry = grouped.setdefault(customer.id, {
                "customer_id": customer.id,
                "customer_name": customer.customer_name,
                "companies": [],
            })
            entry["companies"].append({
                "company_id": company.id,
                "company_name": company.company_name,
            })
        return list(grouped.values())

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'confirm_password', 'role', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    # 1. Field-level validation (runs for both create and update)
    def validate_username(self, value):
        """Validate username is unique and follows rules"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters.")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        return value
    
    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        
        if '@' not in value or '.' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError(
                "Phone number must be in format: +999999999. Up to 15 digits allowed."
            )
        return value

    def validate(self, data):
        """Cross-field validation"""
        # Password validation for create
        if 'password' in data and 'confirm_password' in data:
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            
            if password != confirm_password:
                raise serializers.ValidationError({
                    "confirm_password": "Password fields don't match."
                })
            
            # Additional password strength validation
            if len(password) < 8:
                raise serializers.ValidationError({
                    "password": "Password must be at least 8 characters long."
                })
            
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError({
                    "password": "Password must contain at least one digit."
                })
            
            if not any(char.isupper() for char in password):
                raise serializers.ValidationError({
                    "password": "Password must contain at least one uppercase letter."
                })
        
        return data
    
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['confirm_password']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        """Create user with validated data"""
        # Remove confirm_password if present
        validated_data.pop('confirm_password', None)
        
        # Extract password (required)
        password = validated_data.pop('password')
        
        # Extract role if provided
        role = validated_data.pop('role', None)
        
        # Create user using create_user (handles password hashing)
        user = User.objects.create_user(**validated_data)
        
        # Assign role if provided
        if role:
            user.role = role
            user.save()
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Separate serializer for updates with different validation rules"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
    
    def validate_username(self, value):
        """Username validation for update (exclude current user)"""
        instance = self.instance
        if instance and User.objects.filter(username=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters.")
        
        return value
    
    def validate_email(self, value):
        """Email validation for update"""
        instance = self.instance
        if instance and User.objects.filter(email=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def update(self, instance, validated_data):
        """Update with validation"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserListRequestSerializer(serializers.Serializer):
    """ Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view."""
    search = serializers.CharField(required=False, allow_blank=True, help_text="Name, code ya description mein search karein")
    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')