from django.conf import settings
from django.db import models

from request_management.models import Request


class WorkflowAction(models.Model):

    class ActionType(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        RECEIVED = "RECEIVED", "Received"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        RETURNED = "RETURNED", "Returned"
        STARTED = "STARTED", "Started Processing"
        FORWARDED_TO_ED = "FORWARDED_TO_ED", "Forwarded to ED"
        FORWARDED_TO_CEO = "FORWARDED_TO_CEO", "Forwarded to CEO"
        CEO_APPROVED = "CEO_APPROVED", "CEO Approved"
        CEO_REJECTED = "CEO_REJECTED", "CEO Rejected"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name="workflow_actions",
    )

    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices,
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="workflow_actions",
    )

    from_department = models.ForeignKey(
        "departments.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="workflow_actions_from",
    )

    to_department = models.ForeignKey(
        "departments.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="workflow_actions_to",
    )

    from_status = models.CharField(
        max_length=30,
        blank=True,
    )

    to_status = models.CharField(
        max_length=30,
        blank=True,
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.request.request_number} - "
            f"{self.get_action_type_display()}"
        )