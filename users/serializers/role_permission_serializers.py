from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import User, Role, Module, RolePermission, user,ModuleActionAssoc,Action
from django.core.validators import RegexValidator
import re
from django.core.validators import validate_email


User = get_user_model()
class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields


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

class ModuleActionBasicSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.name', read_only=True)
    module_code = serializers.CharField(source='module.code', read_only=True)
    action_name = serializers.CharField(source='action.name', read_only=True)
    action_code = serializers.CharField(source='action.code', read_only=True)
    class Meta:
        model = ModuleActionAssoc
        fields = ['id', 'module', 'module_code', 'module_name', 'action', 'action_code', 'action_name']
        read_only_fields = fields

#Module Action Assoc Dropdown
class RolePermissionCreateUpdateSerializer(serializers.ModelSerializer):
    module_actions = ModuleActionBasicSerializer(source='module_action_as', many=True, read_only=True)
    class Meta:
        model = RolePermission
        # fields = '__all__'
        fields = ['id', 'role','module_action_assoc','module_actions']#'module','action',
class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    module_action_assoc_detail = ModuleActionBasicSerializer(
        source='module_action_assoc', read_only=True
    )
    class Meta:
        model = RolePermission
        # fields = '__all__' #'module','module_name','module_code','action','action_name',
        fields = [
            'id', 'role', 'role_name', 'role_code',
            'module_action_assoc', 'module_action_assoc_detail',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        ]



class RolePermissionListSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    module_action_assoc_detail = ModuleActionBasicSerializer(
        source='module_action_assoc', read_only=True
    )

    class Meta:
        model = RolePermission
        fields = [
            'id', 'role', 'role_name', 'role_code',
            'module_action_assoc', 'module_action_assoc_detail',
            'created_by', 'created_at', 'updated_by', 'updated_at'
        ]
class ModuleActionDropdownSerializer(serializers.ModelSerializer):
    module = ModuleBasicSerializer(read_only=True)
    action = ActionBasicSerializer(read_only=True)
    class Meta:
        model = ModuleActionAssoc
        # fields = '__all__'
        fields = ['id', 'module','action']
        read_only_fields = fields

    def to_representation(self, instance):
        """
        Output JSON ko manually restructured  for better clarity in response.
        """
        # Original id ko fetch 
        data = super().to_representation(instance)
        
        # make a new custom 'module' dictionary with required fields from both module and action
        custom_module_data = {
            "module_id": instance.module.id,
            "module_name": instance.module.name,
            "module_code": instance.module.code,
            "action_id": instance.action.id,
            "action_name": instance.action.name,
            "action_code": instance.action.code
        }
        #print("Custom module data being returned:", custom_module_data)  # Debug print statement
        # Final structured response return
        return {
            "id": data['id'],
            "module": custom_module_data
        }