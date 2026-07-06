from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import BaseModel
from users.models import User
from master_data.models import Customer

class UserCustomerAssoc(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_customer_assoc')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_user_assoc')


    class Meta:
        db_table = 'user_customer_associations'
        #unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.customer.name} - {self.user.username}"