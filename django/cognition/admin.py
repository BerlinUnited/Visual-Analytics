from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import SingleNumericFilter
from .models import (
    CognitionFrame,
    FrameFilter,
    AudioData,
    BallModel,
    BallCandidates,
    BallCandidatesTop,
    CameraMatrix,
    CameraMatrixTop,
    OdometryData,
    FieldPercept,
    FieldPerceptTop,
    GoalPercept,
    GoalPerceptTop,
    MultiBallPercept,
    RansacCirclePercept2018,
    RansacLinePercept,
    RobotInfo,
    ShortLinePercept,
    ScanLineEdgelPercept,
    ScanLineEdgelPerceptTop,
    TeamMessageDecision,
    Teamstate,
    WhistlePercept,
)


class CognitionFrameAdmin(ModelAdmin):
    search_fields = ["id", "log__id", "frame_number"]
    list_display = ("get_log_id", "get_frame_id", "frame_number")
    ordering = [
        "-id"
    ]  # removes a warning when using this model with autocomplete_fields
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = [
        ("log__id", SingleNumericFilter),
    ]
    # makes sure not all motion frames have to be loaded
    raw_id_fields = ("closest_motion_frame",)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-id")

    def get_log_id(self, obj):
        return obj.log.id

    def get_frame_id(self, obj):
        return obj.id

    get_log_id.short_description = "Log ID"
    get_frame_id.short_description = "Frame ID"


class FrameFilterAdmin(ModelAdmin):
    list_display = ("get_log_id", "get_user", "name")
    list_filter_submit = True
    list_filter = [
        ("log__id", SingleNumericFilter),
    ]

    def get_log_id(self, obj):
        return obj.log.id

    def get_user(self, obj):
        return obj.user

    get_log_id.short_description = "Log ID"
    get_user.short_description = "User"


class CognitionModelAdmin(ModelAdmin):
    list_display = ("get_id", "get_log_id", "get_frame_number")
    list_filter_submit = True
    list_filter = [
        ("frame__log__id", SingleNumericFilter),
        ("frame__frame_number", SingleNumericFilter),
    ]
    autocomplete_fields = ["frame"]

    def get_log_id(self, obj):
        return obj.frame.log.id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    def get_id(self, obj):
        return obj.id

    get_log_id.short_description = "Log ID"
    get_frame_number.short_description = "frame number"


admin.site.register(CognitionFrame, CognitionFrameAdmin)
admin.site.register(FrameFilter, FrameFilterAdmin)
admin.site.register(AudioData, CognitionModelAdmin)
admin.site.register(BallModel, CognitionModelAdmin)
admin.site.register(BallCandidates, CognitionModelAdmin)
admin.site.register(BallCandidatesTop, CognitionModelAdmin)
admin.site.register(CameraMatrix, CognitionModelAdmin)
admin.site.register(CameraMatrixTop, CognitionModelAdmin)
admin.site.register(OdometryData, CognitionModelAdmin)
admin.site.register(FieldPercept, CognitionModelAdmin)
admin.site.register(FieldPerceptTop, CognitionModelAdmin)
admin.site.register(GoalPercept, CognitionModelAdmin)
admin.site.register(GoalPerceptTop, CognitionModelAdmin)
admin.site.register(MultiBallPercept, CognitionModelAdmin)
admin.site.register(RansacCirclePercept2018, CognitionModelAdmin)
admin.site.register(RansacLinePercept, CognitionModelAdmin)
admin.site.register(RobotInfo, CognitionModelAdmin)
admin.site.register(ShortLinePercept, CognitionModelAdmin)
admin.site.register(ScanLineEdgelPercept, CognitionModelAdmin)
admin.site.register(ScanLineEdgelPerceptTop, CognitionModelAdmin)
admin.site.register(TeamMessageDecision, CognitionModelAdmin)
admin.site.register(Teamstate, CognitionModelAdmin)
admin.site.register(WhistlePercept, CognitionModelAdmin)
