from django.db.models import Q

from request_management.models import Request


class DashboardService:

    @staticmethod
    def base_queryset():
        return Request.objects.select_related(
            "created_by",
            "originating_department",
            "destination_department",
        )

    @staticmethod
    def summary(queryset):
        return {
            "total": queryset.count(),

            "draft": queryset.filter(
                status=Request.Status.DRAFT
            ).count(),

            "submitted": queryset.filter(
                status=Request.Status.SUBMITTED
            ).count(),

            "received": queryset.filter(
                status=Request.Status.RECEIVED
            ).count(),

            "under_review": queryset.filter(
                status=Request.Status.UNDER_REVIEW
            ).count(),

            "in_progress": queryset.filter(
                status=Request.Status.IN_PROGRESS
            ).count(),

            "pending_information": queryset.filter(
                status=Request.Status.PENDING_INFORMATION
            ).count(),

            "returned": queryset.filter(
                status=Request.Status.RETURNED
            ).count(),

            "approved": queryset.filter(
                status__in=[
                    Request.Status.APPROVED,
                    Request.Status.CEO_APPROVED,
                ]
            ).count(),

            "rejected": queryset.filter(
                status__in=[
                    Request.Status.REJECTED,
                    Request.Status.CEO_REJECTED,
                ]
            ).count(),

            "completed": queryset.filter(
                status=Request.Status.COMPLETED
            ).count(),

            "cancelled": queryset.filter(
                status=Request.Status.CANCELLED
            ).count(),

            "forwarded_to_ceo": queryset.filter(
                status=Request.Status.FORWARDED_TO_CEO
            ).count(),
        }

    @staticmethod
    def recent_requests(queryset, limit=10):
        requests = queryset.order_by(
            "-created_at"
        )[:limit]

        return [
            {
                "id": request.id,
                "request_number": request.request_number,
                "subject": request.subject,
                "status": request.status,
                "status_label": request.get_status_display(),
                "priority": request.priority,
                "priority_label": request.get_priority_display(),
                "originating_department": (
                    request.originating_department.name
                ),
                "destination_department": (
                    request.destination_department.name
                ),
                "created_by": (
                    request.created_by.get_full_name()
                    or request.created_by.username
                ),
                "created_at": request.created_at,
                "submitted_at": request.submitted_at,
            }
            for request in requests
        ]

    @staticmethod
    def department_dashboard(user):
        department = user.department

        if not department:
            raise ValueError(
                "User is not assigned to a department."
            )

        all_requests = DashboardService.base_queryset().filter(
            Q(originating_department=department)
            | Q(destination_department=department)
        ).distinct()

        sent = DashboardService.base_queryset().filter(
            originating_department=department
        )

        received = DashboardService.base_queryset().filter(
            destination_department=department
        )

        pending = received.filter(
            status__in=[
                Request.Status.SUBMITTED,
                Request.Status.RECEIVED,
                Request.Status.UNDER_REVIEW,
                Request.Status.IN_PROGRESS,
                Request.Status.PENDING_INFORMATION,
            ]
        )

        approved = received.filter(
            status__in=[
                Request.Status.APPROVED,
                Request.Status.CEO_APPROVED,
            ]
        )

        denied = received.filter(
            status__in=[
                Request.Status.REJECTED,
                Request.Status.CEO_REJECTED,
            ]
        )

        return {
            "department": {
                "id": department.id,
                "name": department.name,
                "code": department.code,
            },

            "summary": DashboardService.summary(
                all_requests
            ),

            "sent": sent.count(),
            "received": received.count(),
            "pending": pending.count(),
            "approved": approved.count(),
            "denied": denied.count(),

            "recent_requests": DashboardService.recent_requests(
                all_requests
            ),
        }

    @staticmethod
    def ed_dashboard():
        queryset = DashboardService.base_queryset()

        ed_department = queryset.model.destination_department.field.related_model.objects.filter(
            code="ED",
            is_active=True,
        ).first()

        if not ed_department:
            raise ValueError(
                "Executive Director department is not configured."
            )

        ed_requests = queryset.filter(
            destination_department=ed_department
        )

        awaiting_ed_action = ed_requests.filter(
            status__in=[
                Request.Status.SUBMITTED,
                Request.Status.RECEIVED,
                Request.Status.UNDER_REVIEW,
                Request.Status.IN_PROGRESS,
            ]
        )

        eligible_for_ceo = ed_requests.filter(
            status=Request.Status.APPROVED
        )

        forwarded_to_ceo = queryset.filter(
            status=Request.Status.FORWARDED_TO_CEO
        )

        return {
            "summary": DashboardService.summary(
                queryset
            ),

            "awaiting_ed_action": awaiting_ed_action.count(),

            "eligible_for_ceo_forwarding": (
                eligible_for_ceo.count()
            ),

            "forwarded_to_ceo": forwarded_to_ceo.count(),

            "recent_requests": DashboardService.recent_requests(
                ed_requests
            ),
        }

    @staticmethod
    def ceo_dashboard():
        queryset = DashboardService.base_queryset()

        ceo_requests = queryset.filter(
            destination_department__code="CEO"
        )

        awaiting_ceo = ceo_requests.filter(
            status=Request.Status.FORWARDED_TO_CEO
        )

        approved = ceo_requests.filter(
            status=Request.Status.CEO_APPROVED
        )

        rejected = ceo_requests.filter(
            status=Request.Status.CEO_REJECTED
        )

        return {
            "summary": DashboardService.summary(
                ceo_requests
            ),

            "awaiting_ceo_action": awaiting_ceo.count(),

            "approved_by_ceo": approved.count(),

            "rejected_by_ceo": rejected.count(),

            "recent_requests": DashboardService.recent_requests(
                ceo_requests
            ),
        }