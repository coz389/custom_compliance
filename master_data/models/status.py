from django.db import models
from core.models import BaseModel


# Create your models here.
class Status(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'status'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"
