from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from datetime import datetime

from users.models import User
from master_data.models import InspectionArea


User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = fields

class InspectionAreaListSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = InspectionArea
        # fields = '__all__'
        fields = ['id', 'name','code','start_time','end_time','avg_inspection_time','interval_time','special_operation','status','created_by','created_at', 'updated_by', 'updated_at']


class InspectionAreaListRequestSerializer(serializers.Serializer):
    """ 
    Only for documentation and validation of list endpoint filters and pagination parameters in Swagger. Not used for actual filtering logic in the view 
    """
    search = serializers.CharField(required=False, allow_blank=True, help_text="Search only Name , Code,Start Time ,End Time and Special Operation")
    name = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    start_time = serializers.TimeField(required=False, allow_null=True)
    end_time = serializers.TimeField(required=False, allow_null=True)
    special_operation = serializers.BooleanField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    created_at = serializers.DateField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)
    sort_column = serializers.CharField(required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')


class InspectionAreaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionArea
        # fields = '__all__'
        fields = ['name','code','start_time','end_time','avg_inspection_time','interval_time','special_operation','status']

    
    def validate_name(self, value):
        if InspectionArea.objects.filter(
            name__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Inspection area name already exists."
            )

        return value.strip()

    def validate_code(self, value):
        if InspectionArea.objects.filter(
            code__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Inspection area code already exists."
            )

        return value.strip().upper()

    def validate_avg_inspection_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Average inspection time must be greater than 0."
            )

        return value

    def validate_interval_time(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Interval time cannot be negative."
            )

        return value

    def validate(self, attrs):
        start_time = attrs.get(
            "start_time",
            getattr(self.instance, "start_time", None)
        )

        end_time = attrs.get(
            "end_time",
            getattr(self.instance, "end_time", None)
        )

        avg_inspection_time = attrs.get(
            "avg_inspection_time",
            getattr(self.instance, "avg_inspection_time", None)
        )

        interval_time = attrs.get(
            "interval_time",
            getattr(self.instance, "interval_time", None)
        )

        # End time must be greater than start time
        if start_time >= end_time:
            raise serializers.ValidationError({
                "end_time":
                "End time must be greater than start time."
            })

        # Calculate total operational minutes
        working_minutes = int(
            (
                datetime.combine(datetime.today(), end_time)
                - datetime.combine(datetime.today(), start_time)
            ).total_seconds() / 60
        )

        # Validation for inspection duration
        if avg_inspection_time <= 0:
            raise serializers.ValidationError({
                "avg_inspection_time":
                "Average inspection time must be greater than 0 minutes."
            })

        if interval_time < 0:
            raise serializers.ValidationError({
                "interval_time":
                "Interval time cannot be negative."
            })

        total_slot_minutes = (
            avg_inspection_time +
            interval_time
        )

        # Slot duration should fit within operational hours
        if total_slot_minutes > working_minutes:
            raise serializers.ValidationError({
                "avg_inspection_time":
                (
                    f"Inspection time ({avg_inspection_time} mins) "
                    f"+ interval time ({interval_time} mins) "
                    f"cannot exceed operational hours "
                    f"({working_minutes} mins)."
                )
            })

        # Optional business rule:
        # At least one inspection slot should be possible
        if working_minutes < avg_inspection_time:
            raise serializers.ValidationError({
                "avg_inspection_time":
                (
                    f"Area operational time is only "
                    f"{working_minutes} minutes. "
                    f"At least one inspection slot must fit."
                )
            })

        return attrs

    def create(self, validated_data):
        return InspectionArea.objects.create(
            **validated_data
        )
    


class InspectionAreaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = InspectionArea
        fields = (
            "name",
            "code",
            "start_time",
            "end_time",
            "avg_inspection_time",
            "interval_time",
            "special_operation",
            "status",
        )

    def validate_name(self, value):

        queryset = InspectionArea.objects.filter(
            name__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Inspection area name already exists."
            )

        return value.strip()

    def validate_code(self, value):

        queryset = InspectionArea.objects.filter(
            code__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Inspection area code already exists."
            )

        return value.strip().upper()

    def validate_avg_inspection_time(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Average inspection time must be greater than 0."
            )

        return value

    def validate_interval_time(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Interval time cannot be negative."
            )

        return value

    def validate(self, attrs):

        start_time = attrs.get(
            "start_time",
            self.instance.start_time
        )

        end_time = attrs.get(
            "end_time",
            self.instance.end_time
        )

        if start_time >= end_time:
            raise serializers.ValidationError({
                "end_time":
                "End time must be greater than start time."
            })
        
        working_minutes = int(
            (
                datetime.combine(datetime.today(), end_time)
                - datetime.combine(datetime.today(), start_time)
            ).total_seconds() / 60
        )

        total_slot_minutes = (
            attrs.get(
                "avg_inspection_time",
                self.instance.avg_inspection_time
            )
            +
            attrs.get(
                "interval_time",
                self.instance.interval_time
            )
        )

        if total_slot_minutes > working_minutes:
            raise serializers.ValidationError({
                "avg_inspection_time":
                (
                    "Inspection time + interval time "
                    "cannot exceed operational hours."
                )
            })

        return attrs

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance