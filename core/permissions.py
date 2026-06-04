from rest_framework.permissions import BasePermission
from users.models import RolePermission

class HasModulePermission(BasePermission):
    """
    Custom permission to check if the user has the required action on a specific module.
    Use as: permission_classes = [HasModulePermission]
    Requires view.module_code and view.action_code to be defined.
    """
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Super admin can do everything
        if request.user.role and request.user.role.code == 'super_admin':
            return True

        module_code = getattr(view, 'module_code', None)
        action_code = getattr(view, 'action_code', None)

        # Debugging print (can be removed in production)
        print(f"--- Permission Check ---")
        print(f"User: {request.user.email}")
        print(f"Role: {request.user.role.code if request.user.role else 'None'}")
        print(f"Module: {module_code}")
        print(f"Action: {action_code}")

        if not module_code or not action_code:
            print("Decision: DENIED (Module or Action code missing)")
            return False

        # Check if role permission exists
        has_perm = RolePermission.objects.filter(
            role=request.user.role,
            module__code=module_code,
            action__code=action_code
        ).exists()
        
        print(f"Decision: {'GRANTED' if has_perm else 'DENIED'}")
        return has_perm

class IsAuthorOrAdmin(BasePermission):
    """
    Allow access only to object author or if user has admin+ role.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role and request.user.role.code in ['super_admin', 'admin']:
            return True
        return obj.author == request.user