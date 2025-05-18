from django.db import models
from django.conf import settings # To get the AUTH_USER_MODEL
from common.models import BaseModel # Assuming BaseModel is in common/models.py

class AccessLevel(models.TextChoices):
    """
    Defines the levels of access a role can have for a module.
    Mirrors the AccessLevel Enum from GuardianRoute.DBML.txt.
    """
    NONE = 'NONE', 'No Access'
    VIEW = 'VIEW', 'View Access'
    EDIT = 'EDIT', 'Edit Access'
    # Add other levels if needed, e.g., CREATE, DELETE, MANAGE

class Module(BaseModel):
    """
    Represents a system module or feature area for permission control.
    Mirrors the Module table from GuardianRoute.DBML.txt.
    """
    module_name = models.CharField(max_length=100, unique=True, verbose_name="Internal Module Name", help_text="Internal name used in code, e.g., 'vehicle_management'")
    display_name = models.CharField(max_length=150, verbose_name="Display Name", help_text="User-friendly name for display, e.g., 'Vehicle Management'")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['display_name']

    def __str__(self):
        return self.display_name

class Role(BaseModel):
    """
    Represents a user role within the system.
    Mirrors the Role table from GuardianRoute.DBML.txt.
    Connects to Django's Group model conceptually if needed, or can be standalone.
    """
    # Consider linking to Django's Group model or using it directly:
    # from django.contrib.auth.models import Group
    # group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    # role_name = models.CharField(max_length=150, unique=True, editable=False) # if using Group's name

    role_name = models.CharField(max_length=100, unique=True, verbose_name="Role Name", help_text="e.g., 'Administrator', 'Driver Manager', 'Viewer'")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    # Add a field for default role or system role if needed
    # is_system_role = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ['role_name']

    def __str__(self):
        return self.role_name

    # def save(self, *args, **kwargs):
    #     if hasattr(self, 'group') and self.group: # If using Django Group
    #         self.role_name = self.group.name
    #     super().save(*args, **kwargs)


class UserRole(BaseModel): # This table links Users to Roles (many-to-many)
    """
    Assigns users to roles.
    Mirrors the UserRole table from GuardianRoute.DBML.txt.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')

    class Meta:
        verbose_name = "User Role Assignment"
        verbose_name_plural = "User Role Assignments"
        unique_together = ('user', 'role') # A user can only have a specific role once
        ordering = ['user__email', 'role__role_name']

    def __str__(self):
        return f"{self.user.email} - {self.role.role_name}"


class RolePermission(BaseModel):
    """
    Defines the access level a specific role has for a specific module.
    Mirrors the RolePermission table from GuardianRoute.DBML.txt.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='role_permissions')
    access_level = models.CharField(
        max_length=10,
        choices=AccessLevel.choices,
        default=AccessLevel.NONE,
        verbose_name="Access Level"
    )

    class Meta:
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"
        unique_together = ('role', 'module') # A role can only have one permission level per module
        ordering = ['role__role_name', 'module__display_name']

    def __str__(self):
        return f"{self.role.role_name} - {self.module.display_name}: {self.get_access_level_display()}"

# Note: The actual permission checking logic (like GuardianRoute's ModulePermission)
# would typically reside in a `permissions.py` file within this app or a common app,
# and would query these models.