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


admin.site.register(Company, CustomCompanyAdmin)
