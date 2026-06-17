from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import User, Role, Module, RolePermission, user
from django.core.validators import RegexValidator
import re
from django.core.validators import validate_email


User = get_user_model()
class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields


class LoginSerializer(TokenObtainPairSerializer):

    class Meta:
        pass 
     
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "role_id": user.role.id if user.role else None,
            "role_name": user.role.name if user.role else None,
        }

        privileges = RolePermission.objects.filter(role=user.role).select_related(
            'module_action_assoc__module',
            'module_action_assoc__action'
        )

        privilege_list = [
            f"{p.module_action_assoc.module.code}.{p.module_action_assoc.action.code}".upper()
            for p in privileges
            if p.module_action_assoc  # null check — FK null=True hai
        ]

        custom_data = {
            "access_token": data['access'],
            "user": user_data,
            "user_privileges": privilege_list
        }
        
        return custom_data
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password is required.',
        }
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        error_messages={
            'required': 'Confirm password is required.',
            'blank': 'Confirm password is required.',
        }
    )
    # first_name = serializers.CharField(
    #     required=True, 
    #     allow_blank=False,
    #     error_messages={
    #         'required': 'First name is required.',
    #         'blank': 'First name is required.',
    #     }
    # )
    # last_name = serializers.CharField(
    #     required=True, 
    #     allow_blank=False,
    #     error_messages={
    #         'required': 'Last name is required.',
    #         'blank': 'Last name is required.',
    #     }
    # )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'Email is required.',
                    'blank': 'Email is required.',
                    'invalid': 'Enter a valid email address.',
                }
            },
            'username': {
                'required': True,
                'allow_blank': False,
                'min_length': 3,
                'error_messages': {
                    'required': 'Username is required.',
                    'blank': 'Username is required.',
                    'min_length': 'Username must be at least 3 characters.',
                }
            }
        }

    
    def validate(self, attrs):
        """Cross-field validations for similarity and strength"""
        password = attrs.get('password')
        email = attrs.get('email')
        username = attrs.get('username')
        
        errors = {}
        #Check if password and password2 match at field level to ensure it shows up with other errors
        if password and password !=  attrs.get('password2'):
            errors['password'] = "Passwords do not match."
        
        # Password strength validation (only if they match, which is checked in validate_password2)
        if password and password == attrs.get('password2'):
            try:
                PasswordValidator.validate_strength(password)
                PasswordValidator.validate_common_passwords(password)
            except Exception as e:
                errors['password'] = str(e)
        
        # Email and password similarity check
        if email and password and email.split('@')[0] in password.lower():
            errors['password'] = "Password cannot be too similar to your email"
        
        # Username and password similarity check
        if username and password and username.lower() in password.lower():
            errors['password'] = "Password cannot be too similar to your username"
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        # Assign reader role automatically
        reader_role = Role.objects.get(code='port_user')
        user = User.objects.create_user(
            role=reader_role,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
