from django.contrib import admin
from .models import Annotation
from unfold.admin import ModelAdmin
from django.conf import settings
from unfold.contrib.filters.admin import SingleNumericFilter,ChoicesDropdownFilter,DropdownFilter

class ValidatedDownFilter(DropdownFilter):
    title = "Validated"
    parameter_name = "validated"
    def lookups(self, request, model_admin):
        return [
            ("true", "Validated"),
            ("false", "Not Validated"),
        ]

    def queryset(self, request, queryset):
        value = self.value() # This will be "true", "false", or None
        if value == "true":
            return queryset.filter(validated=True)
        if value == "false":
            return queryset.filter(validated=False)
        # If value is None (no filter selected), or any other unexpected value,
        # return the original queryset
        return queryset
class LogFilter(SingleNumericFilter):
    title = "Log"
    
    def __init__(self,
        field,
        request,
        params,
        model,
        model_admin: ModelAdmin,
        field_path: str,):
        super().__init__(field,request, params, model, model_admin,field_path)
        self.title = 'Log'
        
class ImageFilter(SingleNumericFilter):
    def __init__(self,
        field,
        request,
        params,
        model,
        model_admin: ModelAdmin,
        field_path: str,):
        super().__init__(field,request, params, model, model_admin,field_path)
        self.title = 'Image'

class AnnotationAdmin(ModelAdmin):
    raw_id_fields = ("image",)
    list_per_page = 20
    list_display = ("get_id", "get_log_id", "get_image_id", "get_frame_number", "class_name", "is_empty", "validated", "get_link")
    list_filter_submit = True
    list_filter = [
        ("image__frame__log__id", LogFilter),
        ("image__id",ImageFilter),
        ValidatedDownFilter,
        ("type",ChoicesDropdownFilter)
    ]

    def get_log_id(self, obj):
        return obj.image.frame.log.id

    get_log_id.short_description = "Log ID"

    def get_id(self, obj):
        return obj.id

    get_id.short_description = "ID"

    def get_image_id(self, obj):
        return obj.image.id

    get_image_id.short_description = "Image ID"

    def get_frame_number(self, obj):
        return obj.image.frame.frame_number
    
    get_frame_number.short_description = "Frame number"

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

    get_link.short_description = "Link"
admin.site.register(Annotation, AnnotationAdmin)
