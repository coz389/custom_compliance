from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import InspectionArea
from master_data.serializers import InspectionAreaListSerializer,InspectionAreaListRequestSerializer,InspectionAreaCreateSerializer,InspectionAreaUpdateSerializer



from drf_spectacular.utils import extend_schema # Swagger customization

User = get_user_model()

class InspectionAreaFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    special_operation = django_filters.BooleanFilter()
    status = django_filters.BooleanFilter()
    start_time = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')
    # Date filter: match specific date
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    # Range filter: match between two dates (optional but useful)
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    
    class Meta:
        model = InspectionArea
        fields = ['name','code','start_time','end_time','avg_inspection_time','interval_time','special_operation','status', 'created_by',  'created_at','created_by']


class InspectionAreaListView(generics.GenericAPIView):
    """
    List all inspection area with filtering using POST method
    """
    queryset = InspectionArea.objects.select_related('created_by', 'updated_by').filter(status=True)
    serializer_class = InspectionAreaListSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customs_officer'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=InspectionAreaListRequestSerializer, # Request body schema for filtering and pagination to show in Swagger
        responses={200: InspectionAreaListSerializer(many=True)},
        tags=['Inspection Area Management'], # Grouping in Swagger UI
        description="List all active inspection area with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.", # Detailed description for Swagger UI
        summary="List Inspection Area (with filtering)", # Swagger UI heading for this endpoint
        operation_id="v1_inspection_area_list_post" # URL fragment for this operation in Swagger UI
    )

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Clean request data: strip spaces from keys and values
        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v) 
                      for k, v in request.data.items()}
        
        # 1. Apply filters
        filterset = InspectionAreaFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc') # default to newest first
        
        # Validate sort_column exists in model
        allowed_columns = [f.name for f in InspectionArea._meta.fields]
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
                Q(code__icontains=search) 
            )


        # 3. Custom Pagination
        paginator = self.pagination_class()
        # Get page and page_size from body
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
    

@extend_schema(tags=['Inspection Area Management']) 
class InspectionAreaCreateView(generics.CreateAPIView):
    """
    Create a new inspection area
    """
    queryset = InspectionArea.objects.all()
    serializer_class = InspectionAreaCreateSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'customs_officer'
    action_code = 'add'

    def check_permissions(self, request):
        # Explicitly set action to 'add' for creation
        super().check_permissions(request)



@extend_schema(tags=['Inspection Area Management']) 
class InspectionAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific inspection area
    """
    queryset = InspectionArea.objects.all()
    serializer_class = InspectionAreaListSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'status'
    action_code = 'view'  # default to view, will adjust in check_permissions

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InspectionAreaListSerializer
        return InspectionAreaUpdateSerializer
    
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

    def destroy(self, request, *args, **kwargs):
        # 1. Look up object inside default active manager scope
        instance = self.get_object()
        
        # 3. Execution of the mutation tracking layer
        acting_user = request.user if request.user.is_authenticated else None
        
        # Soft-delete execution boundary
        instance.soft_delete(user=acting_user)
        
        # CRITICAL FIX: Base manager dynamically targeted bypassing soft-delete filtration block
        # explicit backend reload executing base manager
        instance = InspectionArea.all_objects.get(pk=instance.pk)

        # 5. Pipeline Serialization mapping out exact object state representation
        serializer = self.get_serializer(instance)
        
        return Response({
            "status": "success",
            "message": "Inspection area deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

