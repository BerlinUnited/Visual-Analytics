from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VATUser, Organization,EmailVerificationToken,AllowedEmailDomains
from unfold.admin import ModelAdmin

class CustomUserAdmin(UserAdmin,ModelAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("organization",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("organization",)}),)

    # Optionally, display organization in the list view
    list_display = UserAdmin.list_display + ("organization",)


admin.site.register(VATUser, CustomUserAdmin)
admin.site.register(Organization,ModelAdmin)
admin.site.register(EmailVerificationToken,ModelAdmin)
admin.site.register(AllowedEmailDomains,ModelAdmin)