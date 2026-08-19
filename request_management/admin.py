from django.contrib import admin

from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_number",
        "subject",
        "originating_department",
        "destination_department",
        "priority",
        "status",
        "created_by",
        "submitted_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "priority",
        "originating_department",
        "destination_department",
    )

    search_fields = (
        "request_number",
        "subject",
        "description",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
    )

    readonly_fields = (
        "request_number",
        "created_at",
        "submitted_at",
        "received_at",
        "ed_received_at",
        "ed_forwarded_at",
        "ceo_received_at",
        "completed_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Request Information",
            {
                "fields": (
                    "request_number",
                    "subject",
                    "description",
                    "priority",
                    "status",
                )
            },
        ),
        (
            "Routing",
            {
                "fields": (
                    "created_by",
                    "originating_department",
                    "destination_department",
                )
            },
        ),
        (
            "Workflow Timeline",
            {
                "fields": (
                    "created_at",
                    "submitted_at",
                    "received_at",
                    "ed_received_at",
                    "ed_forwarded_at",
                    "ceo_received_at",
                    "completed_at",
                    "updated_at",
                )
            },
        ),
        (
            "Deadline",
            {
                "fields": (
                    "required_by",
                )
            },
        ),
    )