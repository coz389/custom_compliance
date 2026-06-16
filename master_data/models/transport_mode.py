from django.db import models


class TransportMode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=10, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transport_modes'
        managed = False

    def __str__(self):
        return f"{self.name}"
