from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q

from master_data.models import CarrierContact
from master_data.serializers import (CarrierContactSerializer, CarrierContactListSerializer,)

from drf_spectacular.utils import extend_schema


class CarrierContactFilter(django_filters.FilterSet):
    carrier = django_filters.NumberFilter(field_name='carrier_id')
    transport = django_filters.NumberFilter(field_name='transport_id')
    primary_transport = django_filters.NumberFilter(field_name='primary_transport_id')
    customer = django_filters.NumberFilter(field_name='customer_id')
    country = django_filters.NumberFilter(field_name='country_id')
    export_country = django_filters.NumberFilter(field_name='export_country_id')
    import_country = django_filters.NumberFilter(field_name='import_country_id')
    city = django_filters.NumberFilter(field_name='city_id')

    class Meta:
        model = CarrierContact
        fields = [
            'carrier', 'transport', 'primary_transport', 'customer',
            'country', 'export_country', 'import_country', 'city',
            'status', 'auto_approve',
        ]


class CarrierContactListView(generics.GenericAPIView):
    """
    List all carrier contacts with filtering using POST method
    """
    queryset = CarrierContact.objects.select_related(
        'carrier', 'transport', 'primary_transport', 'customer',
        'country', 'export_country', 'import_country', 'city',
        'created_by', 'updated_by'
    ).all()
    serializer_class = CarrierContactSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'carrier_contacts'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=CarrierContactListSerializer,
        responses={200: CarrierContactSerializer(many=True)},
        tags=['Carrier Contacts'],
        description="List all carrier contacts with optional filtering, sorting, and pagination.",
        summary="List Carrier Contacts (with filtering)",
        operation_id="v1_carrier_contacts_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = CarrierContactFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Global search
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(carrier__carrier_name__icontains=search) |
                Q(customer__name__icontains=search) |
                Q(type__icontains=search) |
                Q(shipment_type__icontains=search) |
                Q(service_type__icontains=search) |
                Q(emails__icontains=search)
            )

        # 3. Apply ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in CarrierContact._meta.fields]
        if sort_column in allowed_columns:
            prefix = '-' if sort_order.lower() == 'desc' else ''
            queryset = queryset.order_by(f'{prefix}{sort_column}')

        # 4. Custom Pagination
        paginator = self.pagination_class()
        page_num = clean_data.get('page', 1)
        page_size = clean_data.get('page_size', paginator.page_size)
        paginator.page_size = page_size

        try:
            request.query_params._mutable = True
            request.query_params['page'] = page_num
            request.query_params['page_size'] = page_size
            request.query_params._mutable = False

            page = paginator.paginate_queryset(queryset, request, view=self)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Carrier Contacts'])
class CarrierContactCreateView(generics.CreateAPIView):
    """
    Create a new carrier contact
    """
    queryset = CarrierContact.objects.all()
    serializer_class = CarrierContactSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'carrier_contacts'
    action_code = 'add'

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=['Carrier Contacts'])
class CarrierContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific carrier contact
    """
    queryset = CarrierContact.objects.all()
    serializer_class = CarrierContactSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'carrier_contacts'
    action_code = 'view'

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method in ['PUT', 'PATCH']:
            return 'update'
        elif self.request.method == 'DELETE':
            return 'delete'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        acting_user = request.user if request.user.is_authenticated else None
        instance.soft_delete(user=acting_user)
        instance = CarrierContact.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Carrier contact deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
