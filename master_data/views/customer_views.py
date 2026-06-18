from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import Customer
from master_data.serializers import CustomerSerializer, CustomerListRequestSerializer

from drf_spectacular.utils import extend_schema

User = get_user_model()


class CustomerFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    customer_code = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_code', 'status', 'created_by', 'created_at']


class CustomerListView(generics.GenericAPIView):
    """
    List all customers with filtering using POST method
    """
    queryset = Customer.objects.select_related('created_by', 'updated_by').all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customers'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=CustomerListRequestSerializer,
        responses={200: CustomerSerializer(many=True)},
        tags=['Customer Management'],
        description="List all active customers with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.",
        summary="List Customers (with filtering)",
        operation_id="v1_customer_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = CustomerFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in Customer._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        # Global search
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(customer_name__icontains=search) |
                Q(customer_code__icontains=search)
            )

        # 3. Custom Pagination
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


@extend_schema(tags=['Customer Management'])
class CustomerCreateView(generics.CreateAPIView):
    """
    Create a new customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customers'
    action_code = 'add'

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=['Customer Management'])
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customers'
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
        instance = Customer.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Customer deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
