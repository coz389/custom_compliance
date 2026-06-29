from django.db import models
from core.models import BaseModel


class EmailTemplate(BaseModel):
    status = models.BooleanField(default=True, db_index=True)
    customer = models.ForeignKey('Customer', db_column='customer_id', on_delete=models.CASCADE)
    status_ref = models.ForeignKey('status', db_column='status_id', on_delete=models.CASCADE)
    template_type = models.ForeignKey('EmailTemplateTypes', db_column='template_type', on_delete=models.DO_NOTHING, db_index=True)
    template_title = models.CharField(max_length=255)
    email_to = models.CharField(max_length=255)
    email_cc = models.CharField(max_length=255, null=True, blank=True)
    email_bcc = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    signature = models.TextField(null=True, blank=True)
    signature_logo = models.TextField(null=True, blank=True)
    has_attachment = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_templates'
        ordering = ['id']

    def __str__(self):
        return self.template_title
