from django.db import models


class TransportMode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=10, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='transport_mode_created_by')

    class Meta:
        db_table = 'transport_modes'
        managed = False
        ordering = ['code']

    def __str__(self):
        return f"{self.name}"
