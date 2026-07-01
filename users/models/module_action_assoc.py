from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel
from users.models.action import Action
from users.models.module import Module
from users.models.role import Role

class ModuleActionAssoc(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='moduleaction_assoc')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='actionmodule_assoc')

    class Meta:
        db_table = 'module_actions_assoc'
        unique_together = ('module', 'action')

    def __str__(self):
        return f"{self.module.code} - {self.action.code}"