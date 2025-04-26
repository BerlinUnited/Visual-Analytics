from django.contrib import admin
from .models import Annotation, AnnotationClass
from unfold.admin import ModelAdmin


# Register your models here.
class AnnotationAdmin(ModelAdmin):
    raw_id_fields = ("image",)
    list_per_page = 50

class AnnotationClassAdmin(ModelAdmin):
    list_display = ("name", "color")

admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(AnnotationClass, AnnotationClassAdmin)