from django.db import models
from core.models import BaseModel

from users.models import Role

# Create your models here.
class Customer(BaseModel):
    organization_name = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField(unique=True, max_length=255)
    contact_number = models.CharField(max_length=20, blank=True)
    team_size = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    registration_number = models.CharField(max_length=255, blank=True)
    gst_number = models.CharField(max_length=255, blank=True)

    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = 'master_customers'

    def __str__(self):
        return f"{self.organization_name}"