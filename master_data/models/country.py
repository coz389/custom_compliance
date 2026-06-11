from django.db import models
from core.models import BaseModel


class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    phonecode = models.CharField(max_length=10, blank=True, null=True)
    capital = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=4, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=5, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    timezones = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = 'countries'
        managed = False

    def __str__(self):
        return self.country_name