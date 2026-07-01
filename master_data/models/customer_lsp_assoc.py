from django.db import models
from core.models import BaseModel


class CustomerLspAssoc(BaseModel):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="lsp_assocs", db_column="customer_id",)
    carrier = models.ForeignKey( "Carrier", on_delete=models.PROTECT, related_name="lsp_assocs", db_column="carrier_id",)
    transport = models.ForeignKey("TransportMode", on_delete=models.PROTECT, related_name="lsp_assocs", db_column="transport_id",
        null=True, blank=True,)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "customer_lsp_assoc"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.customer} - {self.carrier}"
