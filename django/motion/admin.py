from django.contrib import admin
from .models import (
    MotionFrame,
    IMUData,
    FSRData,
    ButtonData,
    SensorJointData,
    AccelerometerData,
    InertialSensorData,
    MotionStatus,
    MotorJointData,
    GyrometerData,
)
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import SingleNumericFilter

class MotionFrameAdmin(ModelAdmin):
    search_fields = ["id", "log__id", "frame_number"]
    list_display = ("get_log_id", "get_frame_id", "frame_number")
    ordering = ['-id'] # removes a warning when using this model with autocomplete_fields
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = [
        ("log__id", SingleNumericFilter),
    ]
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-id')
    
    def get_log_id(self, obj):
        return obj.log.id
    
    def get_frame_id(self, obj):
        return obj.id

    get_log_id.short_description = "Log ID"
    get_frame_id.short_description = "Frame ID"


class MotionModelAdmin(ModelAdmin):
    list_display = ("get_id", "get_log_id", "get_frame_number")
    list_filter_submit = True 
    list_filter = [("frame__frame_number",SingleNumericFilter)]
    autocomplete_fields = ["frame"]
    def get_log_id(self, obj):
        return obj.frame.log_id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    def get_id(self, obj):
        return obj.id
    
admin.site.register(MotionFrame,MotionFrameAdmin)
admin.site.register(IMUData,MotionModelAdmin)
admin.site.register(FSRData,MotionModelAdmin)
admin.site.register(ButtonData,MotionModelAdmin)
admin.site.register(SensorJointData,MotionModelAdmin)
admin.site.register(AccelerometerData,MotionModelAdmin)
admin.site.register(InertialSensorData,MotionModelAdmin)
admin.site.register(MotionStatus,MotionModelAdmin)
admin.site.register(MotorJointData,MotionModelAdmin)
admin.site.register(GyrometerData,MotionModelAdmin)
