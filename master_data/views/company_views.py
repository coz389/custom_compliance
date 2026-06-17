from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import Company
from master_data.serializers import CompanySerializer, CompanyListRequestSerializer

from drf_spectacular.utils import extend_schema

User = get_user_model()


class CompanyFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    company_code = django_filters.CharFilter(lookup_expr='icontains')
    domain_name = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Company
        fields = ['company_name', 'company_code', 'customer', 'status', 'created_by', 'created_at']


class CompanyListView(generics.GenericAPIView):
    """
    List all companies with filtering using POST method
    """
    queryset = Company.objects.select_related('customer', 'created_by', 'updated_by').all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'companies'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=CompanyListRequestSerializer,
        responses={200: CompanySerializer(many=True)},
        tags=['Company Management'],
        description="List all active companies with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.",
        summary="List Companies (with filtering)",
        operation_id="v1_company_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = CompanyFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in Company._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        # Global search
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) |
                Q(company_code__icontains=search) |
                Q(domain_name__icontains=search) |
                Q(contact_email__icontains=search)
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


@extend_schema(tags=['Company Management'])
class CompanyCreateView(generics.CreateAPIView):
    """
    Create a new company
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'companies'
    action_code = 'add'

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=['Company Management'])
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific company
    """
    queryset = Company.objects.select_related('customer', 'created_by', 'updated_by').all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'companies'
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
        instance.deleted_by = acting_user
        instance.save(update_fields=['deleted_by'])
        instance.delete()
        return Response(
            {"success": True, "message": "Company deleted successfully."},
            status=status.HTTP_200_OK
        )
