from django.contrib import admin
from .models import Annotation
from unfold.admin import ModelAdmin


# Register your models here.
class AnnotationAdmin(ModelAdmin):
    raw_id_fields = ("image",)
    list_per_page = 50

admin.site.register(Annotation, AnnotationAdmin)
