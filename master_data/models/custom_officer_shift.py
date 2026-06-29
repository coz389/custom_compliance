from django.db import models
from django.core.exceptions import ValidationError
from core.models import BaseModel
from django.core.validators import MinValueValidator

from users.models import User


WORKING_DAYS = [
    ("MON", "Monday"),
    ("TUE", "Tuesday"),
    ("WED", "Wednesday"),
    ("THU", "Thursday"),
    ("FRI", "Friday"),
    ("SAT", "Saturday"),
    ("SUN", "Sunday"),
]

def validate_working_days(value):
    valid_days = {day[0] for day in WORKING_DAYS}

    if not isinstance(value, list):
        raise ValidationError(
            "Working days must be a list."
        )

    invalid_days = set(value) - valid_days

    if invalid_days:
        raise ValidationError(
            f"Invalid day(s): {', '.join(invalid_days)}"
        )


class CustomsOfficerShift(BaseModel):
    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="officer_shifts",
        db_index=True,
        help_text="Customs officer assigned to this shift schedule."
    )
    start_date  = models.DateField(db_index=True, help_text="Date from which this shift schedule becomes effective.")
    end_date  = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Date until which this shift schedule remains effective. Leave blank for an open-ended schedule."
    )
    shift_start_time = models.TimeField(help_text="Daily shift start time in 24-hour format (HH:MM).")
    shift_end_time = models.TimeField(help_text="Daily shift end time in 24-hour format (HH:MM).")
    working_days = models.JSONField(
        default=list,
        validators=[validate_working_days],
        help_text=(
            "Working days. Allowed values: "
            "MON, TUE, WED, THU, FRI, SAT, SUN. "
            "Example: ['MON', 'TUE', 'WED', 'THU', 'FRI']"
        )
    )
    break_time = models.PositiveSmallIntegerField(
        default=30,
        validators=[MinValueValidator(0)],
        help_text="Break duration in minutes during the shift."
    )
    is_available_today = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indicates whether the officer is available for scheduling today."
    )
    status = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Active or inactive status of the shift schedule."
    )
    remarks = models.TextField(
        blank=True
    )

    class Meta:
        db_table = "customs_officer_shifts"
        verbose_name = "Customs Officer Shift"
        verbose_name_plural = "Customs Officer Shifts"
        ordering = ["officer", "start_date"]

    def __str__(self):
        return (
            f"{self.officer.username} | "
            f"{self.shift_start_time} - {self.shift_end_time}"
        )