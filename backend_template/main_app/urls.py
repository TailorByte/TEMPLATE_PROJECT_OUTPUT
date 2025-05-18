from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExampleItemViewSet #, TagViewSet

router = DefaultRouter()
router.register(r'example-items', ExampleItemViewSet, basename='exampleitem')
# router.register(r'tags', TagViewSet, basename='tag') # Uncomment if you have a TagViewSet

app_name = 'main_app'

urlpatterns = [
    path('', include(router.urls)),
    # Add other app-specific URL patterns here
]