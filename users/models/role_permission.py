from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from core.models import BaseModel
from users.models.action import Action
from users.models.module import Module
from users.models.role import Role
from .module_action_assoc import ModuleActionAssoc

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    # module = models.ForeignKey(Module, on_delete=models.CASCADE)
    # action = models.ForeignKey(Action, on_delete=models.CASCADE)
    module_action_assoc = models.ForeignKey(
        ModuleActionAssoc,
        null=True, blank=True,  # Initially null, assign after role creation
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'module_action_assoc',)

    def full_clean(self):
        if (self.module_action_assoc.module_id != self.module_id):
            raise ValidationError("Module mismatch with ModuleActionAssoc.")

        if (self.module_action_assoc.action_id != self.action_id):
            raise ValidationError("Action mismatch with ModuleActionAssoc.")
        
    def save(self, *args, **kwargs):
        # self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role.code} - {self.module.code} - {self.action.code}"