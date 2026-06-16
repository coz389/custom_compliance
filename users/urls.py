from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from users.views import (
    RegisterView, UserProfileView, ChangePasswordView, 
    LogoutView, LogoutAllView,
    UserListView, UserDetailView,UserActiveInactiveView, 
    RoleCreateView,RoleListView, RoleDetailView, 
    ModuleListCreateView, ModuleDetailView, 
    RolePermissionListCreateView, RolePermissionDetailView,RolePermissionCreateView,ModuleActionAssocDropdownView
)



urlpatterns = [
    # Auth
    path('auth/register', RegisterView.as_view(), name='auth_register'),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout', LogoutView.as_view(), name='auth_logout'),
    path('auth/logout-all', LogoutAllView.as_view(), name='logout_all'),
    path('auth/me', UserProfileView.as_view(), name='auth_me'),

    path('auth/change-password', ChangePasswordView.as_view(), name='auth_change_password'),

    # Users (admin)
    path('users', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/toggle-status', UserActiveInactiveView.as_view(), name='user_toggle_status'),

    # Roles
    path('roles', RoleListView.as_view(), name='role_list_filter'),
    path('roles/add', RoleCreateView.as_view(), name='role_create'),
    path('roles/<int:pk>', RoleDetailView.as_view(), name='role_detail'),
    # path('roles/delete/<int:pk>', RoleDetailView.as_view(), name='role_delete'),

    # Modules
    # path('modules', ModuleListCreateView.as_view(), name='module_list'),
    # path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),

    # Role Permissions
    # path('role-permissions', RolePermissionListCreateView.as_view(), name='role_permission_list'),
    path('role-permissions/add', RolePermissionCreateView.as_view(), name='role_permission_create'),
    path('module-action-assoc', ModuleActionAssocDropdownView.as_view(), name='module_action_assoc_list'),
    path('role-permissions/<int:pk>/', RolePermissionDetailView.as_view(), name='role_permission_detail'),
]