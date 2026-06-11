from django.db import models
from core.models import BaseModel
from master_data.models.country import Country
from master_data.models.state import State


class City(BaseModel):
    city_name = models.CharField(max_length=150, unique=True)
    state = models.ForeignKey(
        State,
        db_column='state_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country,
        db_column='country_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.BooleanField(default=True)
    unloc = models.CharField(max_length=20, blank=True)
    utc_offset = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = 'cities'
        managed = False

    def __str__(self):
        return self.city_name
