from django.contrib import admin
from .models import Module, Role, UserRole, RolePermission

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'module_name', 'description', 'created_at', 'updated_at')
    search_fields = ('module_name', 'display_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'created_at', 'updated_at')
    search_fields = ('role_name',)
    readonly_fields = ('created_at', 'updated_at')
    # filter_horizontal = ('permissions',) # If using Django's Group model and m2m to its permissions

class UserRoleInline(admin.TabularInline): # Or admin.StackedInline
    model = UserRole
    extra = 1 # Number of empty forms to display
    autocomplete_fields = ['role'] # If RoleAdmin has search_fields

# If you have a custom UserAdmin in users_app, you might want to add UserRoleInline there.
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# User = get_user_model()
# class CustomUserAdmin(BaseUserAdmin):
#     inlines = [UserRoleInline]
# admin.site.unregister(User) # Unregister the default User admin if it was registered
# admin.site.register(User, CustomUserAdmin) # Register User with the inline

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'updated_at')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'role__role_name')
    autocomplete_fields = ['user', 'role'] # Assumes User and Role admins have search_fields
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module', 'access_level', 'created_at', 'updated_at')
    list_filter = ('role', 'module', 'access_level')
    search_fields = ('role__role_name', 'module__display_name')
    autocomplete_fields = ['role', 'module']
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('access_level',)