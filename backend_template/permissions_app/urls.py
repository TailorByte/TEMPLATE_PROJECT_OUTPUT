from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import ModuleViewSet, RoleViewSet, UserRoleViewSet, RolePermissionViewSet # Uncomment when views are defined

# router = DefaultRouter()
# router.register(r'modules', ModuleViewSet, basename='module')
# router.register(r'roles', RoleViewSet, basename='role')
# router.register(r'user-roles', UserRoleViewSet, basename='userrole')
# router.register(r'role-permissions', RolePermissionViewSet, basename='rolepermission')

app_name = 'permissions_app'

urlpatterns = [
    # path('', include(router.urls)), # Example: Include router URLs
    # Add other app-specific URLs here
]