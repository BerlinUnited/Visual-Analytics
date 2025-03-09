from django.contrib import admin
from .models import NaoImage
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import SingleNumericFilter
# Register your models here.
class ImageAdmin(ModelAdmin):
    search_fields=["get_log_id"]
    list_display = ["get_log_id", "get_frame_number", "camera", "type"]
    list_filter_submit = True 
    list_filter = [("frame__frame_number",SingleNumericFilter)]
    autocomplete_fields = ["frame"]
    def get_log_id(self, obj):
        return obj.frame.log.id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    get_log_id.short_description = "Log ID"
    get_frame_number.short_description = "Frame Number"

admin.site.register(NaoImage, ImageAdmin)
