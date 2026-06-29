from django.db import models
from core.models import BaseModel


class EmailTemplateHash(BaseModel):
    template_type = models.ForeignKey('EmailTemplateTypes', db_column='template_type_id', on_delete=models.DO_NOTHING, db_index=True)
    hash_key = models.CharField(max_length=255)
    hash_title = models.CharField(max_length=255)
    lookup_key = models.CharField(max_length=255)

    class Meta:
        db_table = 'email_template_hashes'

    def __str__(self):
        return f"{self.hash_title} ({self.hash_key})"
