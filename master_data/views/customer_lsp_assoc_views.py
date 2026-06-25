from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q

from master_data.models import CustomerLspAssoc
from master_data.serializers import (CustomerLspAssocSerializer, CustomerLspAssocListSerializer,)

from drf_spectacular.utils import extend_schema


class CustomerLspAssocFilter(django_filters.FilterSet):
    customer = django_filters.NumberFilter(field_name='customer_id')
    carrier = django_filters.NumberFilter(field_name='carrier_id')
    transport = django_filters.NumberFilter(field_name='transport_id')

    class Meta:
        model = CustomerLspAssoc
        fields = ['customer', 'carrier', 'transport', 'status']


class CustomerLspAssocListView(generics.GenericAPIView):
    """
    List all customer-LSP associations with filtering using POST method
    """
    queryset = CustomerLspAssoc.objects.select_related(
        'customer', 'carrier', 'transport',
        'created_by', 'updated_by'
    ).all()
    serializer_class = CustomerLspAssocSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customer_lsp_assoc'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=CustomerLspAssocListSerializer,
        responses={200: CustomerLspAssocSerializer(many=True)},
        tags=['Customer LSP Associations'],
        description="List all customer-LSP associations with optional filtering, sorting, and pagination.",
        summary="List Customer LSP Associations (with filtering)",
        operation_id="v1_customer_lsp_assoc_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = CustomerLspAssocFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Global search
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(customer__customer_name__icontains=search) |
                Q(carrier__carrier_name__icontains=search) |
                Q(transport__name__icontains=search)
            )

        # 3. Apply ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in CustomerLspAssoc._meta.fields]
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


@extend_schema(tags=['Customer LSP Associations'])
class CustomerLspAssocCreateView(generics.CreateAPIView):
    """
    Create a new customer-LSP association
    """
    queryset = CustomerLspAssoc.objects.all()
    serializer_class = CustomerLspAssocSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customer_lsp_assoc'
    action_code = 'add'

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=['Customer LSP Associations'])
class CustomerLspAssocDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific customer-LSP association
    """
    queryset = CustomerLspAssoc.objects.all()
    serializer_class = CustomerLspAssocSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customer_lsp_assoc'
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
        instance = CustomerLspAssoc.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Customer LSP association deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
