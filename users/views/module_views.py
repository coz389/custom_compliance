from rest_framework import generics, permissions
from users.models import Module
from users.serializers import ModuleSerializer
from core.permissions import HasModulePermission

class ModuleListCreateView(generics.ListCreateAPIView):
    """
    List all modules or create a new module (admin only)
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method == 'POST':
            return 'add'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific module (admin only)
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'

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
