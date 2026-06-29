from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from datetime import datetime
from django.db import models
from django.db.models import Q

from users.models import User
from master_data.models import CustomsOfficerShift,WORKING_DAYS

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields

class OfficerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class CustomsOfficerShiftListSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    officer = OfficerBasicSerializer(read_only=True)
    officer_username = serializers.CharField(source="officer.username", read_only=True)
    officer_email = serializers.CharField(source="officer.email", read_only=True)
    class Meta:
        model = CustomsOfficerShift
        # fields = '__all__'
        fields = ['id', 'officer','officer_username','officer_email','start_date','end_date','shift_start_time','shift_end_time','working_days','break_time','status','created_by','created_at', 'updated_by', 'updated_at']


class CustomsOfficerShiftListRequestSerializer(serializers.Serializer):
    """ 
    Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view 
    """
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search only User Name, Email, Remarks ,Start Date ,End Date and Working days")
    officer = serializers.CharField(required=False, allow_blank=True)
    model_name = serializers.CharField(required=False, allow_blank=True)
    action_name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)
    sort_column = serializers.CharField(required=False, default='timestamp')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')



class CustomsOfficerShiftCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsOfficerShift
        # fields = '__all__'
        fields = ['officer','start_date','end_date','shift_start_time','shift_end_time','working_days','break_time','is_available_today','remarks','status']

    
    def validate_working_days(self, value):
        valid_days = {day[0] for day in WORKING_DAYS}

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Working days must be a list."
            )

        if not value:
            raise serializers.ValidationError(
                "At least one working day is required."
            )

        invalid = set(value) - valid_days

        if invalid:
            raise serializers.ValidationError(
                f"Invalid working day(s): {', '.join(sorted(invalid))}"
            )

        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate working days are not allowed."
            )

        return [day.upper() for day in value]

    def validate_break_time(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Break time cannot be negative."
            )

        return value

    def validate(self, attrs):

        officer = attrs.get("officer")

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        shift_start_time = attrs.get("shift_start_time")
        shift_end_time = attrs.get("shift_end_time")

        break_time = attrs.get("break_time")

        # ----------------------------------------
        # Date validation
        # ----------------------------------------

        if end_date and start_date > end_date:
            raise serializers.ValidationError({
                "end_date":
                "End date must be greater than or equal to start date."
            })

        # ----------------------------------------
        # Time validation
        # ----------------------------------------

        if shift_start_time >= shift_end_time:
            raise serializers.ValidationError({
                "shift_end_time":
                "Shift end time must be greater than shift start time."
            })

        shift_minutes = int(
            (
                datetime.combine(datetime.today(), shift_end_time)
                - datetime.combine(datetime.today(), shift_start_time)
            ).total_seconds() / 60
        )

        if break_time >= shift_minutes:
            raise serializers.ValidationError({
                "break_time":
                "Break time cannot be greater than or equal to shift duration."
            })

        # ----------------------------------------
        # Overlapping shift validation
        # ----------------------------------------

        overlap = CustomsOfficerShift.objects.filter(
            officer=officer,
            status=True,
        )

        if end_date:
            overlap = overlap.filter(
                start_date__lte=end_date
            )

        overlap = overlap.filter(
            Q(end_date__isnull=True) |
            Q(end_date__gte=start_date)
        )

        if overlap.exists():
            raise serializers.ValidationError({
                "officer":
                "An overlapping shift already exists for this officer."
            })

        return attrs

    def create(self, validated_data):
        return CustomsOfficerShift.objects.create(
            **validated_data
        )
    

class CustomsOfficerShiftUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomsOfficerShift
        fields = ['officer','start_date','end_date','shift_start_time','shift_end_time','working_days','break_time','is_available_today','remarks','status']

    
    def validate_working_days(self, value):

        valid_days = {day[0] for day in WORKING_DAYS}

        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Working days must be a list."
            )

        if not value:
            raise serializers.ValidationError(
                "At least one working day is required."
            )

        invalid = set(value) - valid_days

        if invalid:
            raise serializers.ValidationError(
                f"Invalid working day(s): {', '.join(sorted(invalid))}"
            )

        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate working days are not allowed."
            )

        return [day.upper() for day in value]

    def validate_break_time(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Break time cannot be negative."
            )

        return value

    def validate(self, attrs):

        officer = attrs.get(
            "officer",
            self.instance.officer
        )

        start_date = attrs.get(
            "start_date",
            self.instance.start_date
        )

        end_date = attrs.get(
            "end_date",
            self.instance.end_date
        )

        shift_start_time = attrs.get(
            "shift_start_time",
            self.instance.shift_start_time
        )

        shift_end_time = attrs.get(
            "shift_end_time",
            self.instance.shift_end_time
        )

        break_time = attrs.get(
            "break_time",
            self.instance.break_time
        )

        # ------------------------------------
        # Date Validation
        # ------------------------------------

        if end_date and start_date > end_date:
            raise serializers.ValidationError({
                "end_date":
                "End date must be greater than or equal to start date."
            })

        # ------------------------------------
        # Time Validation
        # ------------------------------------

        if shift_start_time >= shift_end_time:
            raise serializers.ValidationError({
                "shift_end_time":
                "Shift end time must be greater than shift start time."
            })

        shift_minutes = int(
            (
                datetime.combine(datetime.today(), shift_end_time)
                - datetime.combine(datetime.today(), shift_start_time)
            ).total_seconds() / 60
        )

        if break_time >= shift_minutes:
            raise serializers.ValidationError({
                "break_time":
                "Break time cannot be greater than or equal to shift duration."
            })

        # ------------------------------------
        # Overlapping Shift Validation
        # ------------------------------------

        overlap = CustomsOfficerShift.objects.filter(
            officer=officer,
            status=True,
        ).exclude(
            pk=self.instance.pk
        )

        if end_date:
            overlap = overlap.filter(
                start_date__lte=end_date
            )

        overlap = overlap.filter(
            Q(end_date__isnull=True) |
            Q(end_date__gte=start_date)
        )

        if overlap.exists():
            raise serializers.ValidationError({
                "officer":
                "An overlapping shift already exists for this officer."
            })

        return attrs

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance