from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import SubStatus
from master_data.serializers import (
    SubStatusListRequestSerializer,
    SubStatusSerializer,
    SubStatusUpdateSerializer,
)

from drf_spectacular.utils import extend_schema  # Swagger customization

User = get_user_model()


class SubStatusFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    # Date filter: match specific date
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    # Range filter: match between two dates (optional but useful)
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = SubStatus
        fields = ['name', 'created_by', 'status', 'created_at']


class SubStatusListView(generics.GenericAPIView):
    """
    List all sub status with filtering using POST method
    """
    queryset = SubStatus.objects.select_related('created_by', 'updated_by').filter(status=True)
    serializer_class = SubStatusSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'sub_status'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=SubStatusListRequestSerializer,  # Request body schema for filtering and pagination to show in Swagger
        responses={200: SubStatusSerializer(many=True)},
        tags=['Sub Status Management'],  # Grouping in Swagger UI
        description="List all active sub status with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.",  # Detailed description for Swagger UI
        summary="List Sub Status (with filtering)",  # Swagger UI heading for this endpoint
        operation_id="v1_sub_status_list_post"  # URL fragment for this operation in Swagger UI
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Clean request data: strip spaces from keys and values
        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = SubStatusFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')  # default to newest first

        # Validate sort_column exists in model
        allowed_columns = [f.name for f in SubStatus._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        # --- GLOBAL SEARCH LOGIC ---
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # 3. Custom Pagination
        paginator = self.pagination_class()
        # Get page and page_size from body
        page_num = clean_data.get('page', 1)
        page_size = clean_data.get('page_size', paginator.page_size)

        # Override paginator attributes for this request
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


@extend_schema(tags=['Sub Status Management'])
class SubStatusDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a specific sub status (description only)
    """
    queryset = SubStatus.objects.all()
    serializer_class = SubStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'sub_status'
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
        instance = SubStatus.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)

        return Response({
            "status": "success",
            "message": "Sub Status deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
