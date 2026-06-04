from .auth_views import RegisterView,UserProfileView, ChangePasswordView
from .user_views import UserListCreateView,UserDetailView
from .role_views import RoleListView, RoleCreateView, RoleDetailView
from .module_views import ModuleListCreateView, ModuleDetailView
from .permission_views import RolePermissionListCreateView, RolePermissionDetailView

__all__ = [
    # Auth views
    'RegisterView',
    'UserProfileView',
    'ChangePasswordView',
    # User views
    'UserListCreateView',
    'UserDetailView',
    # Role views
    'RoleListView',
    'RoleCreateView',
    'RoleDetailView',
    # Module views
    'ModuleListCreateView',
    'ModuleDetailView',
    # Permission views
    'RolePermissionListCreateView',
    'RolePermissionDetailView',
]
