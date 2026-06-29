from django.db import models


class EmailTemplateTypes(models.Model):
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'email_template_types'
        ordering = ['id']

    def __str__(self):
        return self.title
