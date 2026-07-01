from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q

from master_data.models.transport_mode import TransportMode
from master_data.serializers.transport_mode_serializers import (
    TransportModeSerializer,
    TransportModeListRequestSerializer,
)

from drf_spectacular.utils import extend_schema


class TransportModeFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TransportMode
        fields = ['code', 'name', 'status']


class TransportModeListView(generics.GenericAPIView):
    """
    List all transport modes with filtering using POST method
    """
    queryset = TransportMode.objects.all()
    serializer_class = TransportModeSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'transport_modes'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=TransportModeListRequestSerializer,
        responses={200: TransportModeSerializer(many=True)},
        tags=['Transport Mode Management'],
        description="List all transport modes with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.",
        summary="List Transport Modes (with filtering)",
        operation_id="v1_transport_mode_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        # 1. Apply filters
        filterset = TransportModeFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in TransportMode._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        # Global search
        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search)
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
