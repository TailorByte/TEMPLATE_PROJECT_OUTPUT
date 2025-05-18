from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        # Fields to include in the serialized output
        fields = [
            'id', # Or 'user_id' if your PK is named differently in DBML but 'id' in model
            'email', 
            'first_name', 
            'last_name', 
            'is_active', 
            'is_staff', 
            'is_superuser',
            'date_joined',
            'last_login',
            # Add any other custom fields you want to expose
            # 'activation_token', # Usually not exposed directly
            # 'activation_expiry',  # Usually not exposed directly
        ]
        # Make certain fields read-only if they shouldn't be updated via API directly
        read_only_fields = ('date_joined', 'last_login', 'is_staff', 'is_superuser') 

    def create(self, validated_data):
        # Handle password hashing during user creation
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Handle password updates carefully if allowed via this serializer
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

# Example Serializer for Account Activation (Conceptual)
# class AccountActivationSerializer(serializers.Serializer):
#     token = serializers.UUIDField(required=True)

# Example Serializer for Password Reset Request (Conceptual)
# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

# Example Serializer for Password Reset Confirm (Conceptual)
# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.UUIDField(required=True)
#     new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
#     confirm_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

#     def validate(self, data):
#         if data['new_password'] != data['confirm_password']:
#             raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
#         # Add password complexity validation here if needed
#         return data