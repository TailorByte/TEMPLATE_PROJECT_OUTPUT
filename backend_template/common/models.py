from django.db import models

class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated At")

    class Meta:
        abstract = True
        ordering = ['-created_at'] # Default ordering for models inheriting this

# Example of how other models could inherit from BaseModel:
#
# from .models import BaseModel # Assuming BaseModel is in the same app's models.py
#
# class MySpecificModel(BaseModel):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name