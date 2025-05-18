from rest_framework import viewsets, permissions
# from rest_framework.decorators import action
# from rest_framework.response import Response
from .models import ExampleItem #, Tag
from .serializers import ExampleItemSerializer #, TagSerializer
# from common.permissions import IsOwnerOrReadOnly # Example custom permission from a common app

class ExampleItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ExampleItems to be viewed or edited.
    """
    queryset = ExampleItem.objects.all().order_by('-created_at')
    serializer_class = ExampleItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Example permission

    # If you added an 'owner' field to ExampleItem, you might want to set it automatically:
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    # Example custom action:
    # @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    # def toggle_active(self, request, pk=None):
    #     item = self.get_object()
    #     item.is_active = not item.is_active
    #     item.save()
    #     return Response({'status': 'active status toggled', 'is_active': item.is_active})

# Example TagViewSet if you have a Tag model
# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all().order_by('name')
#     serializer_class = TagSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]