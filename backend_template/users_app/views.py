from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
# from .serializers import UserSerializer # Uncomment when UserSerializer is created
# from common.permissions import IsOwnerOrReadOnly # Example custom permission

User = get_user_model()

# Example ViewSet for User model (customize as needed)
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer # Replace with your UserSerializer
#     permission_classes = [permissions.IsAdminUser] # Example: Only admins can manage users

    # Example custom action:
    # @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    # def me(self, request):
    #     """
    #     Return the authenticated user's data.
    #     """
    #     serializer = self.get_serializer(request.user)
    #     return Response(serializer.data)

# Add other views for user management, e.g., registration, password reset, activation, etc.
# These might be API views or traditional Django views depending on your needs.

# Example: Account Activation View (Conceptual - needs a serializer and URL)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from .serializers import AccountActivationSerializer # Create this serializer

# class AccountActivationView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = AccountActivationSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = User.objects.get(activation_token=serializer.validated_data['token'], is_active=False)
#                 if user.activation_expiry < timezone.now():
#                     return Response({'detail': 'Activation link has expired.'}, status=status.HTTP_400_BAD_REQUEST)
                
#                 user.is_active = True
#                 user.clear_activation_token()
#                 user.save()
#                 return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response({'detail': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Remember to create serializers (e.g., UserSerializer, AccountActivationSerializer) in users_app/serializers.py
# and URL patterns in users_app/urls.py