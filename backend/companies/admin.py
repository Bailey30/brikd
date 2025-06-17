from django.contrib import admin
from common.models import BaseUser
from companies.models import Company


## Register your models here.
# @admin.register(BaseUser)
class CustomCompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = [
        "email",
        "name",
        "is_admin",
        "is_active",
        "created_at",
        "updated_at",
    ]

    def email(self, obj):
        return obj.profile.email

    def is_admin(self, obj):
        return obj.profile.is_admin

    def is_active(self, obj):
        return obj.profile.is_active

    def created_at(self, obj):
        return obj.profile.created_at

    def updated_at(self, obj):
        return obj.profile.updated_at


admin.site.register(Company, CustomCompanyAdmin)
