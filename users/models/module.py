from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel

class Module(BaseModel):
    name = models.CharField(max_length=100, unique=True)  # Posts, Tags, Comments
    code = models.CharField(max_length=50, unique=True)   # posts, tags, comments
    icon = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)  # active/inactive
    
    class Meta:
        db_table = 'modules'

    def __str__(self):
        return self.name