from django.db import models
from core.models import BaseModel
from master_data.models import customer


class Company(BaseModel):
    customer = models.ForeignKey(customer.Customer, db_column='customer_id', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, unique=True)
    company_code = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    domain_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return f"{self.company_name}"