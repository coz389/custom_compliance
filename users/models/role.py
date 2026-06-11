from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel

class Role(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    code = models.CharField(max_length=80, unique=True)  # super_admin, admin, author, reader
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)  # active/inactive

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name