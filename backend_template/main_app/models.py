from django.db import models
from django.conf import settings # To get the AUTH_USER_MODEL
from common.models import BaseModel # Import the BaseModel from the common app

class ExampleItem(BaseModel):
    """
    An example model for the main application.
    Inherits created_at and updated_at from BaseModel.
    """
    name = models.CharField(max_length=255, verbose_name="Item Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    # Example of a ForeignKey to the custom User model
    # owner = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL, # Or models.CASCADE, models.PROTECT, etc.
    #     related_name='example_items',
    #     null=True,
    #     blank=True,
    #     verbose_name="Owner"
    # )

    # Example of a ManyToManyField
    # tags = models.ManyToManyField('Tag', blank=True, related_name='example_items')

    class Meta:
        verbose_name = "Example Item"
        verbose_name_plural = "Example Items"
        ordering = ['name'] # Default ordering

    def __str__(self):
        return self.name

# Example Tag model if you uncomment the ManyToManyField above
# class Tag(BaseModel):
#     name = models.CharField(max_length=100, unique=True)
#
#     class Meta:
#         verbose_name = "Tag"
#         verbose_name_plural = "Tags"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name