from django.contrib import admin
from .models import *

class BallModelAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'get_log_id', 'get_frame_number')

    def get_log_id(self, obj):
        return obj.frame.log_id
    
    def get_frame_number(self, obj):
        return obj.frame.frame_number

    def get_id(self, obj):
        return obj.id

admin.site.register(CognitionFrame)
admin.site.register(BallModel, BallModelAdmin)

admin.site.register(BallCandidates)
admin.site.register(BallCandidatesTop)
admin.site.register(CameraMatrix)
admin.site.register(CameraMatrixTop)
admin.site.register(OdometryData)
admin.site.register(FieldPercept)
admin.site.register(FieldPerceptTop)
admin.site.register(GoalPercept)
admin.site.register(GoalPerceptTop)
admin.site.register(MultiBallPercept)
admin.site.register(RansacLinePercept)
admin.site.register(ShortLinePercept)
admin.site.register(ScanLineEdgelPercept)
admin.site.register(ScanLineEdgelPerceptTop)
admin.site.register(RansacCirclePercept2018)