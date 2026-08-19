from django.contrib.auth.models import AbstractUser
from django.db import models

from departments.models import Department


class User(AbstractUser):

    class Role(models.TextChoices):
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Administrator"
        CEO = "CEO", "Chief Executive Officer"
        EXECUTIVE_DIRECTOR = "EXECUTIVE_DIRECTOR", "Executive Director"
        DEPARTMENT_HEAD = "DEPARTMENT_HEAD", "Department Head"
        DEPARTMENT_OFFICER = "DEPARTMENT_OFFICER", "Department Officer"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.DEPARTMENT_OFFICER,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    is_active_employee = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name() or self.username
    