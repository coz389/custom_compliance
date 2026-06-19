from django.db import models
from core.models import BaseModel
from master_data.models.transport_mode import TransportMode


class Carrier(BaseModel):
    type = models.CharField(max_length=50, blank=True)
    carrier_name = models.CharField(max_length=255, unique=True)
    carrier_scac = models.CharField(max_length=100, blank=True)
    web_link = models.CharField(max_length=255, blank=True)
    transport = models.ForeignKey(
        TransportMode,
        db_column='transport_id',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='carriers',
    )
    logo = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'master_carriers'

    def __str__(self):
        return f"{self.carrier_name}"
