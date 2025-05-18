from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for the custom User model.
    Uses email as the username field.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Use the default UserAdmin fieldsets, but adjust for email as username
    # Remove 'username' if it's in fieldsets, as it's set to None in the model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Activation & Reset Tokens', {'fields': ('activation_token', 'activation_expiry', 'password_reset_token', 'password_reset_expiry')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    # Make token fields read-only in the admin as they are managed by model methods
    readonly_fields = ('last_login', 'date_joined', 'activation_token', 'activation_expiry', 'password_reset_token', 'password_reset_expiry')

# If you have other models in users_app, register them here.