from django.db import models
from core.models import BaseModel
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class InspectionArea(BaseModel):
    name = models.CharField(
        max_length=250,
        unique=True,
        db_index=True,
        help_text="Inspection area name."
    )
    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique inspection area code."
    )

    start_time = models.TimeField(
        db_index=True,
        help_text="Operational start time in 24-hour format."
    )

    end_time = models.TimeField(
        db_index=True,
        help_text="Operational end time in 24-hour format."
    )

    avg_inspection_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Average inspection duration in minutes."
    )

    interval_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Buffer/break time between inspections in minutes."
    )

    special_operation = models.BooleanField(
        default=False,
        help_text="Indicates whether the area supports special inspection operations."
    )

    status = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Active/Inactive status."
    )

    class Meta:
        db_table = "inspection_areas"
        verbose_name = "Inspection Area"
        verbose_name_plural = "Inspection Areas"
        ordering = ["name"]

    def __str__(self):
        return (
            f"{self.name} | "
            f"{self.start_time} - {self.end_time}"
        )