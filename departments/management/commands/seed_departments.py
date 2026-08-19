from django.core.management.base import BaseCommand

from departments.models import Department


DEPARTMENTS = [
    {
        "name": "CEO",
        "code": "CEO",
        "department_type": Department.DepartmentType.EXECUTIVE,
        "description": "Chief Executive Officer",
    },
    {
        "name": "Executive Director",
        "code": "ED",
        "department_type": Department.DepartmentType.EXECUTIVE,
        "description": "Executive Director",
    },
    {
        "name": "Regulations & Compliance",
        "code": "R&C",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Regulations and Compliance",
    },
    {
        "name": "Program and Planning",
        "code": "P&P",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Program and Planning",
    },
    {
        "name": "Sector Coordination",
        "code": "SC",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Sector Coordination",
    },
    {
        "name": "General Services",
        "code": "GS",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "General Services",
    },
    {
        "name": "Administration",
        "code": "ADMIN",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Administration",
    },
    {
        "name": "Procurement",
        "code": "PROC",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Procurement",
    },
    {
        "name": "Finance",
        "code": "FIN",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Finance",
    },
    {
        "name": "Communication",
        "code": "COMM",
        "department_type": Department.DepartmentType.DEPARTMENT,
        "description": "Communication",
    },
]


class Command(BaseCommand):
    help = "Create the official NWASHC departments."

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for department_data in DEPARTMENTS:
            department, created = Department.objects.get_or_create(
                code=department_data["code"],
                defaults={
                    "name": department_data["name"],
                    "department_type": department_data["department_type"],
                    "description": department_data["description"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {department.name}"
                    )
                )
            else:
                existing_count += 1
                self.stdout.write(
                    f"Already exists: {department.name}"
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Complete. Created: {created_count}, "
                f"Already existed: {existing_count}"
            )
        )