from django.contrib import admin
from .models import NaoImage
from unfold.admin import ModelAdmin

# Register your models here.
class ImageAdmin(ModelAdmin):
    list_display = ["get_log_id", "get_frame_number", "camera", "type"]
    
    def get_log_id(self, obj):
        return obj.frame.log.id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    get_log_id.short_description = "Log ID"
    get_frame_number.short_description = "Frame Number"
    
admin.site.register(NaoImage, ImageAdmin)
