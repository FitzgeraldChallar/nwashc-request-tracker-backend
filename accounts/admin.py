from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "department",
        "is_active_employee",
        "is_active",
    )

    list_filter = (
        "role",
        "department",
        "is_active_employee",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Commission Information",
            {
                "fields": (
                    "role",
                    "department",
                    "phone",
                    "profile_photo",
                    "is_active_employee",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Commission Information",
            {
                "fields": (
                    "role",
                    "department",
                    "phone",
                    "profile_photo",
                    "is_active_employee",
                )
            },
        ),
    )