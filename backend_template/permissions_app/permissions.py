from rest_framework.permissions import BasePermission
# from .models import RolePermission, AccessLevel # Assuming models are in the same app

class ModulePermission(BasePermission):
    """
    Custom permission to check if the user has the required access level
    for a specific module.

    Usage in a ViewSet:
    permission_classes = [IsAuthenticated, ModulePermission]
    module_name = "your_module_internal_name" # Define this in your ViewSet

    Or, for action-specific permissions:
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ModulePermission], module_name="specific_action_module")
    def my_action(self, request):
        ...
    """
    required_access_level = AccessLevel.VIEW # Default to VIEW, can be overridden in ViewSet

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers have all permissions
        if request.user.is_superuser:
            return True

        module_name = getattr(view, 'module_name', None)
        if not module_name:
            # If module_name is not defined on the view, deny access by default
            # Or, you could allow access if no module_name is specified, depending on policy
            # For safety, let's deny if not specified.
            # print(f"Warning: module_name not set on view {view.__class__.__name__} for ModulePermission check.")
            return False

        # Determine the required access level for the current action
        action_required_level_str = getattr(view, 'action_required_access_level', {}).get(view.action)
        
        required_level = self.required_access_level # Default for the ViewSet
        if action_required_level_str:
            try:
                required_level = AccessLevel[action_required_level_str.upper()]
            except KeyError:
                # print(f"Warning: Invalid access level string '{action_required_level_str}' for action {view.action} in view {view.__class__.__name__}")
                return False # Invalid level string

        # Check user's roles and their permissions for the module
        # This is a simplified check. A more robust implementation might cache user permissions.
        user_roles = request.user.user_roles.all() # Assumes related_name='user_roles' on UserRole model
        if not user_roles.exists():
            return False # User has no roles assigned

        for user_role_assignment in user_roles:
            role = user_role_assignment.role
            try:
                role_perm = RolePermission.objects.get(role=role, module__module_name=module_name)
                
                # Simple hierarchy: EDIT implies VIEW
                if required_level == AccessLevel.VIEW:
                    if role_perm.access_level in [AccessLevel.VIEW, AccessLevel.EDIT]:
                        return True
                elif required_level == AccessLevel.EDIT:
                    if role_perm.access_level == AccessLevel.EDIT:
                        return True
                # Add more levels if necessary
                        
            except RolePermission.DoesNotExist:
                continue # This role has no specific permission for this module

        return False

    def has_object_permission(self, request, view, obj):
        # Object-level permissions are not typically handled by this ModulePermission directly.
        # This permission is more for view-level access based on module and role.
        # You might implement IsOwnerOrReadOnly or similar for object-level checks.
        # For now, if view-level permission is granted, allow object access.
        return self.has_permission(request, view)

# Example of how to use AccessLevel enum if it's defined in models.py
from .models import AccessLevel, RolePermission