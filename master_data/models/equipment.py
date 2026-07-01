from django.db import models

from core.models import BaseModel


class Equipment(BaseModel):
    code = models.CharField(max_length=80, unique=True)
    type = models.CharField(max_length=80, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "equipments"
        managed = False
        ordering = ['-updated_at']

    def __str__(self):
        return self.code
