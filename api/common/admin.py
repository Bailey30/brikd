from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from common.models import BaseUser
from companies.models import Company


# Register your models here.
@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    model = Company
    list_display = ["email", "is_admin", "is_active", "created_at", "updated_at"]
