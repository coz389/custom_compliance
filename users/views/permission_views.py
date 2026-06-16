from rest_framework import generics, permissions
from users.models import RolePermission
from users.serializers import RolePermissionSerializer,RolePermissionCreateUpdateSerializer
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from users.serializers import ModuleActionDropdownSerializer
from users.models import ModuleActionAssoc


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
    serializer_class = RolePermissionSerializer
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
        elif self.request.method in ['PUT', 'PATCH']:
            return 'update'
        # elif self.request.method == 'DELETE':
        #     return 'delete'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

@extend_schema(
    responses={200: ModuleActionDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of Module Action.",
    summary="Module Action Dropdown",
    operation_id="v1_module_action_list",
)
class ModuleActionAssocDropdownView(generics.ListAPIView):
    queryset = ModuleActionAssoc.objects.all()
    serializer_class = ModuleActionDropdownSerializer
    pagination_class = None
    filter_backends = []  # Disable search, ordering, filters
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "user_roles"
    action_code = "view"