from django.contrib import admin

from vectors.models import ImageVector


@admin.register(ImageVector)
class ImageVectorAdmin(admin.ModelAdmin):
    list_display = ["filename"]
