from django.db import models


class Department(models.Model):
    class DepartmentType(models.TextChoices):
        EXECUTIVE = "EXECUTIVE", "Executive"
        DEPARTMENT = "DEPARTMENT", "Department"

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=30, unique=True)
    department_type = models.CharField(
        max_length=20,
        choices=DepartmentType.choices,
        default=DepartmentType.DEPARTMENT,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name