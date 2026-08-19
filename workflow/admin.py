from django.contrib import admin

from .models import WorkflowAction


@admin.register(WorkflowAction)
class WorkflowActionAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "action_type",
        "performed_by",
        "from_department",
        "to_department",
        "from_status",
        "to_status",
        "created_at",
    )

    list_filter = (
        "action_type",
        "from_department",
        "to_department",
    )

    search_fields = (
        "request__request_number",
        "request__subject",
        "performed_by__username",
        "comment",
    )

    readonly_fields = (
        "request",
        "action_type",
        "performed_by",
        "from_department",
        "to_department",
        "from_status",
        "to_status",
        "comment",
        "created_at",
    )

    ordering = ("-created_at",)