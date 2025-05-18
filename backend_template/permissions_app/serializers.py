from rest_framework import serializers
from .models import Module, Role, UserRole, RolePermission #, AccessLevel

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'module_name', 'display_name', 'description', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name', 'description', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

class UserRoleSerializer(serializers.ModelSerializer):
    # user_email = serializers.EmailField(source='user.email', read_only=True) # Example
    # role_name = serializers.CharField(source='role.role_name', read_only=True) # Example

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'created_at', 'updated_at'] # 'user_email', 'role_name'
        read_only_fields = ('created_at', 'updated_at')

class RolePermissionSerializer(serializers.ModelSerializer):
    # role_name = serializers.CharField(source='role.role_name', read_only=True) # Example
    # module_display_name = serializers.CharField(source='module.display_name', read_only=True) # Example
    # access_level_display = serializers.CharField(source='get_access_level_display', read_only=True) # Example

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'module', 'access_level', 'created_at', 'updated_at'] # 'role_name', 'module_display_name', 'access_level_display'
        read_only_fields = ('created_at', 'updated_at')

# Add other serializers as needed, e.g., for assigning roles to users,
# or for managing permissions for a role.