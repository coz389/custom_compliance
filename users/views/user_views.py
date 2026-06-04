from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, UserCreateSerializer
from core.permissions import HasModulePermission

User = get_user_model()

class UserListCreateView(generics.ListCreateAPIView):
    """
    List all users or create a new user (admin only)
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method == 'POST':
            return 'add'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific user (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
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

    def perform_destroy(self, instance):
        # Soft delete
        instance.soft_delete(user=self.request.user)