from django.db import models
from core.models import BaseModel


class CustomerDocAssoc(BaseModel):
    customer = models.ForeignKey( "Customer", on_delete=models.CASCADE, related_name="document_type_assocs", db_column="customer_id",)
    document_type = models.ForeignKey( "DocumentType", on_delete=models.CASCADE, related_name="customer_assocs", db_column="document_type_id",)
    export_country = models.ForeignKey( "Country", on_delete=models.PROTECT, related_name="export_document_assocs", db_column="export_country_id", null=True, blank=True,)
    import_country = models.ForeignKey( "Country", on_delete=models.PROTECT, related_name="import_document_assocs", db_column="import_country_id", null=True, blank=True,)

    class Meta:
        db_table = "customer_doc_assoc"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.customer} - {self.document_type}"
