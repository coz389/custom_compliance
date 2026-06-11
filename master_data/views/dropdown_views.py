from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions

from core.permissions import HasModulePermission
from master_data.models.country import Country
from master_data.models.state import State
from master_data.serializers.dropdown_serializers import (
    CountryDropdownSerializer,
    StateDropdownSerializer,
)


@extend_schema(
    responses={200: CountryDropdownSerializer(many=True)},
    tags=["Country Management"],
    description="Dropdown list of countries.",
    summary="Country Dropdown",
    operation_id="v1_country_list",
)
class CountryDropdownView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("country_name")
    serializer_class = CountryDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "country"
    action_code = "view"


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="country_id",
            description="Country id used to filter states.",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name="state_name",
            description="Optional case-insensitive state name search.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: StateDropdownSerializer(many=True)},
    tags=["State Management"],
    description="Dropdown list of states filtered by country.",
    summary="State Dropdown",
    operation_id="v1_state_list",
)
class StateDropdownView(generics.ListAPIView):
    serializer_class = StateDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "country"
    action_code = "view"

    def get_queryset(self):
        queryset = State.objects.filter(country_id=self.kwargs.get("country_id"))
        state_name = self.request.query_params.get("state_name", "").strip()

        if state_name:
            queryset = queryset.filter(state_name__icontains=state_name)

        return queryset.order_by("state_name")
