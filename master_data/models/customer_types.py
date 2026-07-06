from django.db import models
from core.models import BaseModel


class Customer(models.Model):
    customer_type = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    domain_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f"{self.name}"