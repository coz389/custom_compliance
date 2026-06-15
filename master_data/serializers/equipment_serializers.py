from rest_framework import serializers

from master_data.models.equipment import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    updated_by = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Equipment
        fields = [
            "id",
            "status",
            "code",
            "type",
            "description",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]


class EquipmentListRequestSerializer(serializers.Serializer):
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search by code, type or description",
    )
    code = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    sort_column = serializers.CharField(required=False, default="created_at")
    sort_order = serializers.ChoiceField(
        choices=["asc", "desc"], required=False, default="desc"
    )
