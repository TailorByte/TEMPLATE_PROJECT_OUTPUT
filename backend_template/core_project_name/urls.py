"""
URL configuration for core_project_name project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # To serve media files during development
from django.conf.urls.static import static # To serve media files during development

# For API Documentation (drf-spectacular)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# For JWT Authentication (rest_framework_simplejwt)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    # TokenBlacklistView, # Uncomment if you implement a blacklist view directly
)

# Placeholder for API v1 URLs from local apps
# Example:
# api_v1_urlpatterns = [
#     path('main/', include('main_app.urls')),
#     path('users/', include('users_app.urls')),
#     # Add other app URLs here
# ]

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 Endpoints
    # path('api/v1/', include(api_v1_urlpatterns)), # Uncomment and define api_v1_urlpatterns when apps are ready

    # JWT Token Authentication Endpoints (as seen in GuardianRoute.API_Mapping.txt)
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/v1/auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # If needed

    # API Schema & Documentation (drf-spectacular)
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # TODO: Add other project-wide URLs here (e.g., for account activation, password reset if not part of an app)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Also serve collected static if needed for dev