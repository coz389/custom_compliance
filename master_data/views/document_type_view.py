from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import DocumentType
from master_data.serializers import DocumentTypeSerializer, DocumentTypeListRequestSerializer


from drf_spectacular.utils import extend_schema,extend_schema_view # Swagger customization

User = get_user_model()

class DocumentTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    # Date filter: match specific date
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    # Range filter: match between two dates (optional but useful)
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    
    class Meta:
        model = DocumentType
        fields = ['name','transport_mode', 'created_by', 'status', 'created_at','created_by']



class DocumentTypeListView(generics.GenericAPIView):
    """
    List all document type with filtering using POST method
    """
    queryset = DocumentType.objects.select_related('created_by', 'updated_by')
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'document_type'
    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=DocumentTypeListRequestSerializer, # Request body schema for filtering and pagination to show in Swagger
        responses={200: DocumentTypeSerializer(many=True)},
        tags=['Document Management'], # Grouping in Swagger UI
        description="List all active Document Types with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.", # Detailed description for Swagger UI
        summary="List Document Type (with filtering)", # Swagger UI heading for this endpoint
        operation_id="v1_document_type_list_post" # URL fragment for this operation in Swagger UI
    )

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Clean request data: strip spaces from keys and values
        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v) 
                      for k, v in request.data.items()}
        
        # 1. Apply filters
        filterset = DocumentTypeFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc') # default to newest first
        
        # Validate sort_column exists in model
        allowed_columns = [f.name for f in DocumentType._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')


        # --- GLOBAL SEARCH LOGIC ---
        search = clean_data.get('search')
        if search:
            # Yeh name, code, ya description mein se kahin bhi match karega (OR condition)
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
        
        # We need to trick DRF paginator to read page from our clean_data instead of query_params
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
            error_msg = str(e)
            if 'Invalid page' in error_msg or 'invalid page' in error_msg.lower():
                return Response({
                    "status": 200,
                    "message": "Data not found",
                    "results": {"detail": "No data found"}
                }, status=status.HTTP_200_OK)
            return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Document Management']) 
class DocumentTypeCreateView(generics.CreateAPIView):
    """
    Create a new Document Type (admin only)
    """
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'document_type'
    action_code = 'add'

    def check_permissions(self, request):
        # Explicitly set action to 'add' for creation
        super().check_permissions(request)

@extend_schema(tags=['Document Management']) 
class DocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific status (admin only)
    """
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'document_type'
    action_code = 'view'  # default to view, will adjust in check_permissions

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
        # 1. Look up object inside default active manager scope
        instance = self.get_object()
        
        # 3. Execution of the mutation tracking layer
        acting_user = request.user if request.user.is_authenticated else None
        
        # Soft-delete execution boundary
        instance.soft_delete(user=acting_user)
        
        # CRITICAL FIX: Base manager dynamically targeted bypassing soft-delete filtration block
        # explicit backend reload executing base manager
        instance = DocumentType.all_objects.get(pk=instance.pk)

        # 5. Pipeline Serialization mapping out exact object state representation
        serializer = self.get_serializer(instance)
        
        return Response({
            "status": "success",
            "message": "Status deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema_view( get=extend_schema(
    responses={200: DocumentTypeSerializer(many=False)},
    tags=["Dropdown lists"],
    description="Dropdown list of active document types.",
    summary="Document type Dropdown",
    operation_id="v1_document_type_list_dropdown",
))
class DocumentTypeDropdownView(generics.ListAPIView):
    serializer_class = DocumentTypeSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "document_type"
    action_code = "view"
    
    queryset = DocumentType.objects.filter(status=True).order_by('name')