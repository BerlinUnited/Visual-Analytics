from django.contrib import admin
from .models import Annotation
from unfold.admin import ModelAdmin
from django.conf import settings


# Register your models here.
class AnnotationAdmin(ModelAdmin):
    raw_id_fields = ("image",)
    list_display = ("get_id", "get_log_id", "get_image_id", "get_frame_number", "class_name", "is_empty", "validated", "get_link")

    def get_id(self, obj):
        return obj.image.frame.log.id

    def get_log_id(self, obj):
        return obj.id

    def get_image_id(self, obj):
        return obj.image.id

    def get_frame_number(self, obj):
        return obj.image.frame.frame_number

    def get_link(self, obj):
        # Determine the domain and scheme
        if settings.DEBUG:
            # Development - use localhost
            domain = "127.0.0.1:8000"
            scheme = "http"
        else:
            # Production - use your actual domain
            domain = "vat.berlin-united.com"  # Replace with your actual domain
            scheme = "https"
        return f"{scheme}://{domain}/log/{obj.image.frame.log.id}/frame/{obj.image.frame.frame_number}?filter=None"

admin.site.register(Annotation, AnnotationAdmin)
