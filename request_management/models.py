from django.conf import settings
from django.db import models

from departments.models import Department


class Request(models.Model):

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        NORMAL = "NORMAL", "Normal"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        RECEIVED = "RECEIVED", "Received"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        PENDING_INFORMATION = "PENDING_INFORMATION", "Pending Information"
        RETURNED = "RETURNED", "Returned"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        FORWARDED_TO_ED = "FORWARDED_TO_ED", "Forwarded to ED"
        FORWARDED_TO_CEO = "FORWARDED_TO_CEO", "Forwarded to CEO"
        CEO_APPROVED = "CEO_APPROVED", "CEO Approved"
        CEO_REJECTED = "CEO_REJECTED", "CEO Rejected"
        COMPLETED = "COMPLETED", "Completed"
        CLOSED = "CLOSED", "Closed"
        CANCELLED = "CANCELLED", "Cancelled"

    request_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    subject = models.CharField(max_length=255)

    description = models.TextField()

    request_document = models.FileField(
        upload_to="request_documents/",
        null=True,
        blank=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # Person who originally created the request
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_requests",
    )

    # Department where the request originated
    originating_department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="originated_requests",
    )

    # Current destination department
    destination_department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="received_requests",
    )

    # Important workflow timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    received_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    ed_received_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    ed_forwarded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    ceo_received_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    required_by = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.request_number} - {self.subject}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            super().save(*args, **kwargs)

            year = self.created_at.year
            self.request_number = (
                f"NWASHC-REQ-{year}-{self.pk:06d}"
            )

            super().save(
                update_fields=["request_number"]
            )

            return

        super().save(*args, **kwargs)
        