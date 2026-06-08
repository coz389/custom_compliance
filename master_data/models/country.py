from django.db import models
from core.models import BaseModel


# Create your models here.
class Customer(BaseModel):
    country_name = models.CharField(max_length=255, unique=True)
    iso3 = models.CharField(max_length=20, blank=True)
    iso2 = models.CharField(max_length=20, blank=True)
    phone_code = models.CharField(max_length=20, blank=True)
    region = models.EmailField(unique=True, max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_countries'

    def __str__(self):
        return f"{self.organization_name}"
