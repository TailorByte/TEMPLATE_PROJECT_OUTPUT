from rest_framework import serializers
from .models import ExampleItem #, Tag # Import your app's models

class ExampleItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ExampleItem model.
    """
    # Example of a nested serializer or a string representation for related fields
    # owner_email = serializers.EmailField(source='owner.email', read_only=True, allow_null=True)
    # tags = serializers.StringRelatedField(many=True, read_only=True) # Or use a TagSerializer

    class Meta:
        model = ExampleItem
        fields = [
            'id', 
            'name', 
            'description', 
            'is_active', 
            # 'owner', # If you have an owner ForeignKey, include its ID for write operations
            # 'owner_email', # Read-only representation of owner's email
            # 'tags', # Read-only representation of tags
            'created_at', 
            'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at') # Audit fields are typically read-only

# Example TagSerializer if you have a Tag model
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name']