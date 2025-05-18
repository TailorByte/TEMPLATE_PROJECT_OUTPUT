from django.contrib import admin
from .models import ExampleItem # Import your app's models

@admin.register(ExampleItem)
class ExampleItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at') # Customize as needed
    list_filter = ('is_active', 'created_at') # Customize as needed
    search_fields = ('name', 'description') # Customize as needed
    readonly_fields = ('created_at', 'updated_at') # Common for audit fields
    # fieldsets = ( ... ) # Define custom layout for the edit page if needed

# Register other models from this app here
# from .models import Tag
# admin.site.register(Tag)