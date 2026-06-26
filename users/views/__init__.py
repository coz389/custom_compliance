from .auth_views import RegisterView,UserProfileView, ChangePasswordView, LogoutView, LogoutAllView,LoginView
from .user_views import UserListView,UserDetailView,UserListRequestSerializer,UserActiveInactiveView,UserListByRoleDropdownView
from .role_views import RoleListView, RoleCreateView, RoleDetailView
from .module_views import ModuleListCreateView, ModuleDetailView
from .permission_views import RolePermissionListCreateView,RolePermissionCreateView, RolePermissionDetailView,ModuleActionAssocDropdownView,RolePermissionListView,BulkRolePermissionView


__all__ = [
    # Auth views
    'LoginView',
    'RegisterView',
    'UserProfileView',
    'ChangePasswordView',
    'LogoutView',
    'LogoutAllView',
    # User views
    'UserListView',
    'UserDetailView',
    'UserListRequestSerializer',
    'UserActiveInactiveView',
    'UserListByRoleDropdownView',
    # Role views
    'RoleListView',
    'RoleCreateView',
    'RoleDetailView',
    # Module views
    'ModuleListCreateView',
    'ModuleDetailView',
    # Permission views
    'RolePermissionListCreateView',
    'RolePermissionCreateView',
    'RolePermissionDetailView',
    'ModuleActionAssocDropdownView',
    'RolePermissionListView',
    'BulkRolePermissionView',
]
