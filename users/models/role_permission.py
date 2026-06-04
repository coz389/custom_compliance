from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel
from users.models.action import Action
from users.models.module import Module
from users.models.role import Role

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'module', 'action')

    def __str__(self):
        return f"{self.role.code} - {self.module.code} - {self.action.code}"