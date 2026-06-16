from django.db import models

from core.models import BaseModel
from master_data.models.transport_mode import TransportMode


class Container(BaseModel):
    transport = models.ForeignKey(
        TransportMode,
        db_column="transport_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    code = models.CharField(max_length=5, blank=True)
    iso = models.CharField(max_length=50, blank=True)
    net_weight = models.DecimalField(max_digits=14, decimal_places=3, null=True, blank=True)
    net_volume = models.DecimalField(max_digits=14, decimal_places=3, null=True, blank=True)
    size = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, null=True)
    dimension = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    

    class Meta:
        db_table = "containers"
        managed = False

    def __str__(self):
        return self.code
