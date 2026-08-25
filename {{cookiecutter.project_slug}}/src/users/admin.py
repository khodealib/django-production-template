from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "first_name", "last_name", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "date_joined"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-date_joined"]
    fieldsets = (
        *(BaseUserAdmin.fieldsets or ()),
        ("Extra", {"fields": ()}),
    )
    add_fieldsets = (
        *(BaseUserAdmin.add_fieldsets or ()),
        ("Extra", {"fields": ("email",)}),
    )
