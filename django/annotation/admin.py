from django.contrib import admin
from .models import Annotation
from unfold.admin import ModelAdmin


# Register your models here.
class AnnotationAdmin(ModelAdmin):
    raw_id_fields = ("image",)
    list_display = ("get_id", "get_image_id", "get_frame_number", "class_name", "is_empty", "validated")

    def get_id(self, obj):
        return obj.id

    def get_image_id(self, obj):
        return obj.image.id

    def get_frame_number(self, obj):
        return obj.image.frame.frame_number

admin.site.register(Annotation, AnnotationAdmin)
