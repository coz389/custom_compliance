from django.db import models
from core.models import BaseModel
from master_data.models.country import Country


class State(models.Model):
    state_name = models.CharField(max_length=150, unique=True)
    country = models.ForeignKey(Country, db_column='country_id', on_delete=models.CASCADE)
    country_code = models.CharField(max_length=3, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = 'states'
        managed = False

    def __str__(self):
        return self.state_name