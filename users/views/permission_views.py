from rest_framework import generics, permissions,status,serializers as drf_serializers
from users.models import RolePermission
from users.serializers import RolePermissionSerializer,RolePermissionCreateUpdateSerializer,RolePermissionListSerializer
from core.permissions import HasModulePermission
from rest_framework.views import APIView
import django_filters
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view, inline_serializer, OpenApiExample
from users.serializers import ModuleActionDropdownSerializer
from users.models import ModuleActionAssoc,Role


class RolePermissionFilter(django_filters.FilterSet):
    role_code = django_filters.CharFilter(field_name='role__code',lookup_expr='icontains')
    # module_code = django_filters.CharFilter(field_name='module__code',lookup_expr='icontains')
    # action_name = django_filters.CharFilter(field_name='action__name',lookup_expr='icontains')
    # Date filter: match specific date
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    # Range filter: match between two dates (optional but useful)
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    
    class Meta:
        model = RolePermission
        fields = ['id', 'role','role_code','created_by','created_at'] #'module','module_code','action','action_name',



class RolePermissionListView(generics.GenericAPIView):
    """
    List all roles with filtering using POST method
    """
    queryset = RolePermission.objects.select_related('created_by', 'updated_by')
    serializer_class = RolePermissionListSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_roles'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=RolePermissionListSerializer, # Request body schema for filtering and pagination to show in Swagger
        responses={200: RolePermissionListSerializer(many=True)},
        tags=['Roles Permission Management'], # Grouping in Swagger UI
        description="List all active roles permission with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.", # Detailed description for Swagger UI
        summary="List Roles Permission (with filtering)", # Swagger UI heading for this endpoint
        operation_id="v1_role_permission_list_post" # URL fragment for this operation in Swagger UI
    )

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Clean request data: strip spaces from keys and values
        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v) 
                      for k, v in request.data.items()}
        
        # 1. Apply filters
        filterset = RolePermissionFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Apply Custom Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc') # default to newest first
        
        # Validate sort_column exists in model
        allowed_columns = [f.name for f in RolePermission._meta.fields]
        if sort_column in allowed_columns:
            prefix = '-' if sort_order.lower() == 'desc' else ''
            queryset = queryset.order_by(f'{prefix}{sort_column}')
        else:
            queryset = queryset.order_by(f'{sort_column}')  # safe default


        # --- GLOBAL SEARCH LOGIC ---
        search = clean_data.get('search')
        if search:
            # Yeh name, code, ya description mein se kahin bhi match karega (OR condition)
            queryset = queryset.filter(
                Q(role__name__icontains=search) |
                Q(role__code__icontains=search) |
                Q(module__name__icontains=search) |
                Q(module__code__icontains=search) |
                Q(action__name__icontains=search)
            )


        # 3. Custom Pagination
        paginator = self.pagination_class()
        # Get page and page_size from body
        page_num = clean_data.get('page', 1)
        page_size = clean_data.get('page_size', paginator.page_size)
        
        # Override paginator attributes for this request
        paginator.page_size = page_size
        
        # We need to trick DRF paginator to read page from our clean_data instead of query_params
        # Or we can manually paginate
        try:
            # Standard paginator uses query_params, so we override the request's query_params temporarily
            # But a cleaner way is to set the page number manually if possible.
            # For simplicity, let's inject into request.query_params for the paginator to find it
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



class RolePermissionListCreateView(generics.ListCreateAPIView):
    """
    List all role permissions or create new role permissions (admin only)
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_roles'

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method == 'POST':
            return 'add'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

# @extend_schema(tags=['Role Management']) 
class RolePermissionCreateView(generics.CreateAPIView):
    """
    Create a new status (admin only)
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_roles'
    action_code = 'add'

    def check_permissions(self, request):
        # Explicitly set action to 'add' for creation
        super().check_permissions(request)

class RolePermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific role permission (admin only)
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer #
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_roles'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RolePermissionCreateUpdateSerializer
        # for others default serializer
        return self.serializer_class
    
    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        # elif self.request.method in ['PUT', 'PATCH']:
        #     return 'update'
        # elif self.request.method == 'DELETE':
        #     return 'delete'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)




@extend_schema(
    tags=['Roles Management'],
    request=inline_serializer(
        name='BulkRolePermissionRequest',
        fields={
            'module_action_assoc': drf_serializers.ListField(
                child=drf_serializers.IntegerField(min_value=1),
                help_text='List of ModuleActionAssoc IDs to assign to this role.',
            )
        }
    ),
    examples=[
        OpenApiExample(
            name='Assign permissions',
            value={'module_action_assoc': [1, 2, 3]},
            request_only=True,
        )
    ],
    summary='Bulk assign permissions to a role',
    description='Replaces all existing permissions for the role with the provided list.',
)
class BulkRolePermissionView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_roles'

    def get_action_code(self):
        return 'update'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    def put(self, request, role_id):
        role = get_object_or_404(Role, pk=role_id)
        assoc_ids = request.data.get('module_action_assoc', [])

        if not isinstance(assoc_ids, list) or not assoc_ids:
            return Response(
                {"module_action_assoc": "Must be a non-empty list of IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        assocs = ModuleActionAssoc.objects.filter(id__in=assoc_ids)
        if assocs.count() != len(assoc_ids):
            return Response(
                {"module_action_assoc": "One or more IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            RolePermission.objects.filter(role=role).delete()
            RolePermission.objects.bulk_create([
                RolePermission(
                    role=role,
                    module_action_assoc=assoc,
                    created_by=request.user
                )
                for assoc in assocs
            ])
        # ✅ Created records fetch data to serialize
        # created = RolePermission.objects.filter(role=role).select_related(
        #     'role', 'module_action_assoc'
        # )
        created = RolePermission.objects.filter(role=role).select_related(
            'role',
            'module_action_assoc',
            'module_action_assoc__module',
            'module_action_assoc__action'
        )
        serializer = RolePermissionListSerializer(created, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema_view(get=extend_schema(
    responses={200: ModuleActionDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of Module Action.",
    summary="Module Action Dropdown",
    operation_id="v1_module_action_list",
))
class ModuleActionAssocDropdownView(generics.ListAPIView):
    queryset = ModuleActionAssoc.objects.all()
    serializer_class = ModuleActionDropdownSerializer
    pagination_class = None
    filter_backends = []  # Disable search, ordering, filters
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "user_roles"
    action_code = "view"