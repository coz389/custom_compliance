from django.db import models
from core.models import BaseModel


# Create your models here.
class DocumentType(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    transport_mode = models.ForeignKey(
        'TransportMode',
        on_delete=models.PROTECT,
        null=True, blank=True,  # Initially null, assign after role creation
        related_name='transport_mode',
        db_column="transport_mode_id"
    )
    file_formats = models.JSONField(default=list)  # stores ["pdf", "xls", "csv"]
    description = models.CharField(max_length=255, blank=True)
    required_for_refer = models.BooleanField(default=False)
    required_for_dg = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'document_types'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"
