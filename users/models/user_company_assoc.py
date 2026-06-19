from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel
from users.models.action import Action
from users.models.user import User
from master_data.models import Company

class UserCompanyAssoc(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_company_assoc')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_user_assoc')
    
    class Meta:
        db_table = 'user_company_associations'
        #unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.company.company_name} - {self.user.username}"