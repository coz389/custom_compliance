from django.db import models
from core.models import BaseModel


class CarrierContact(BaseModel):
    carrier = models.ForeignKey(
        "Carrier", on_delete=models.CASCADE, related_name="carrier_contacts", db_column="carrier_id",
    )
    type = models.CharField(max_length=20, blank=True)
    transport = models.ForeignKey(
        "TransportMode", on_delete=models.PROTECT, related_name="carrier_contacts_transport",
        db_column="transport_id", null=True, blank=True,
    )
    shipment_type = models.CharField(max_length=20, blank=True)
    primary_transport = models.ForeignKey(
        "TransportMode", on_delete=models.PROTECT, related_name="carrier_contacts_primary_transport",
        db_column="primary_transport_id", null=True, blank=True,
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="carrier_contacts",
        db_column="customer_id", null=True, blank=True,
    )
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="carrier_contacts",
        db_column="company_id", null=True, blank=True,
    )
    country = models.ForeignKey(
        "Country", on_delete=models.SET_NULL, related_name="carrier_contacts_country",
        db_column="country_id", null=True, blank=True,
    )
    emails = models.TextField(blank=True)
    export_country = models.ForeignKey(
        "Country", on_delete=models.SET_NULL, related_name="carrier_contacts_export",
        db_column="export_country_id", null=True, blank=True,
    )
    import_country = models.ForeignKey(
        "Country", on_delete=models.SET_NULL, related_name="carrier_contacts_import",
        db_column="import_country_id", null=True, blank=True,
    )
    city = models.ForeignKey(
        "City", on_delete=models.SET_NULL, related_name="carrier_contacts",
        db_column="city_id", null=True, blank=True,
    )
    service_type = models.CharField(max_length=50, blank=True)
    threshold = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    auto_approve = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "carrier_contacts"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.carrier} - {self.type}"
