from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions

from core.permissions import HasModulePermission
from master_data.models.country import Country
from master_data.models.equipment import Equipment
from master_data.models.state import State
from master_data.serializers.dropdown_serializers import (
    CountryDropdownSerializer,
    EquipmentDropdownSerializer,
    StateDropdownSerializer,
    CustomerDropdownSerializer
)
from master_data.models import Customer,Company

@extend_schema(
    responses={200: CountryDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of countries.",
    summary="Country Dropdown",
    operation_id="v1_country_list",
)
class CountryDropdownView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("country_name")
    serializer_class = CountryDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "countries"
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
    tags=["Dropdown lists"],
    description="Dropdown list of states filtered by country.",
    summary="State Dropdown",
    operation_id="v1_state_list",
)
class StateDropdownView(generics.ListAPIView):
    serializer_class = StateDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "countries"
    action_code = "view"

    def get_queryset(self):
        queryset = State.objects.filter(country_id=self.kwargs.get("country_id"))
        state_name = self.request.query_params.get("state_name", "").strip()

        if state_name:
            queryset = queryset.filter(state_name__icontains=state_name)

        return queryset.order_by("state_name")


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="search",
            description="Optional case-insensitive search by equipment code or type.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: EquipmentDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of active equipment items.",
    summary="Equipment Dropdown",
    operation_id="v1_equipment_list_dropdown",
)
class EquipmentDropdownView(generics.ListAPIView):
    serializer_class = EquipmentDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "package_management"
    action_code = "view"

    def get_queryset(self):
        queryset = Equipment.objects.filter(status=True)
        search = self.request.query_params.get("search", "").strip()

        if search:
            queryset = queryset.filter(Q(code__icontains=search) | Q(type__icontains=search))

        return queryset.order_by("code")


@extend_schema(
    responses={200: CustomerDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of customer & companies.",
    summary="Customer & Company Dropdown",
    operation_id="v1_customer_company_list",
)
class CustomerDropdownView(generics.ListAPIView):
    serializer_class = CustomerDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "companies"
    action_code = "view"
    
    queryset = Customer.objects.filter(deleted_at__isnull=True, status=True).order_by('customer_name')

