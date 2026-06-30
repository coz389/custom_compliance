from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, permissions

from core.permissions import HasModulePermission
from master_data.models import Country, State, Equipment, Customer, TransportMode
from master_data.serializers import (
    CountryDropdownSerializer,
    CustomerDropdownSerializer,
    EquipmentDropdownSerializer,
    StateDropdownSerializer,
    TransportModeBasicSerializer,
    CustomerCompanyDropdownSerializer,
)


@extend_schema_view( get=extend_schema(
    parameters=[
        OpenApiParameter(
            name="country_name",
            description="Optional case-insensitive country name search.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: CountryDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of countries.",
    summary="Country Dropdown",
    operation_id="v1_country_list",
))
class CountryDropdownView(generics.ListAPIView):
    serializer_class = CountryDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "countries"
    action_code = "view"

    def get_queryset(self):
        queryset = Country.objects.all()
        country_name = self.request.query_params.get("country_name", "").strip()

        if country_name:
            queryset = queryset.filter(country_name__icontains=country_name)

        return queryset.order_by("country_name")


@extend_schema_view( get=extend_schema(
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
))
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

@extend_schema_view(get=extend_schema(
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
))
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


@extend_schema_view(get=extend_schema(
    parameters=[
        OpenApiParameter(
            name="customer_name",
            description="Optional case-insensitive customer name search.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: CustomerDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of active customers.",
    summary="Customer Dropdown",
    operation_id="v1_customer_list_dropdown",
))
class CustomerDropdownView(generics.ListAPIView):
    serializer_class = CustomerDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "customers"
    action_code = "view"
    def get_queryset(self):
        queryset = Customer.objects.filter(status=True)
        customer_name = self.request.query_params.get("customer_name", "").strip()

        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)

        return queryset.order_by("customer_name")


@extend_schema_view(get=extend_schema(
    parameters=[
        OpenApiParameter(
            name="customer_name",
            description="Optional case-insensitive customer name search.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: CustomerCompanyDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of active customers.",
    summary="Customer Company Dropdown",
    operation_id="v1_customer_company_list_dropdown",
))
class CustomerCompaniesDropdownView(generics.ListAPIView):
    serializer_class = CustomerCompanyDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "customers"
    action_code = "view"
    queryset = Customer.objects.filter(deleted_at__isnull=True, status=True).order_by('customer_name')
    
@extend_schema_view(get=extend_schema(
    responses={200: TransportModeBasicSerializer(many=False)},
    tags=["Dropdown lists"],
    description="Dropdown list of active transport modes.",
    summary="Transport mode Dropdown",
    operation_id="v1_transport_mode_list_dropdown",
))
class TransportModeDropdownView(generics.ListAPIView):
    serializer_class = TransportModeBasicSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "transport_modes"
    action_code = "view"
    
    # queryset = TransportMode.objects.filter(status=True).order_by('name')
    def get_queryset(self):
        queryset = TransportMode.objects.filter(status=True)
        search = self.request.query_params.get("search", "").strip()
 
        if search:
            queryset = queryset.filter(Q(code__icontains=search) | Q(name__icontains=search))
 
        return queryset.order_by("name")


