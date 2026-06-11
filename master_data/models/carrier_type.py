from django.db import models
from core.models import BaseModel


class CarrierType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'carrier_types'

    def __str__(self):
        return f"{self.name}"