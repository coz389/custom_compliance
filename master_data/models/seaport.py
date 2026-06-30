from django.db import models

from core.models import BaseModel
from master_data.models.country import Country


class Seaport(BaseModel):
    port_name = models.CharField(max_length=150)
    unloc = models.CharField(max_length=20, blank=True)
    utc_offset = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        db_column="country_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tradelane_name = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "master_sea_ports"
        managed = False
        ordering = ['-updated_at']

    def __str__(self):
        return self.port_name
