from rest_framework import serializers
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



class RolePermissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        # fields = '__all__'
        fields = ['id', 'role','module','action']
class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        # fields = '__all__'
        fields = ['id', 'role','module','action','created_by','created_at', 'updated_by', 'updated_at']