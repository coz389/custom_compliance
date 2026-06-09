from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel

class Action(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    code = models.CharField(max_length=80, unique=True)  # view, add, change, delete
    status = models.BooleanField(default=True)  # active/inactive
    
    class Meta:
        db_table = 'actions'

    def __str__(self):
        return self.name