from django.db import models
from core.models import BaseModel

class CustomerContact(BaseModel):
    status = models.BooleanField(default=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='contacts', db_index=True)
    transport_mode = models.CharField(max_length=50, blank=True, null=True)
    service_type = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    port = models.ForeignKey('Seaport', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'customer_contacts'

    def __str__(self):
        return f"{self.email}"