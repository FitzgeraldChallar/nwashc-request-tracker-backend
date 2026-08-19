from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from departments.models import Department
from request_management.models import Request

from .models import WorkflowAction


class RequestWorkflowService:

    @staticmethod
    def _record_action(
        request,
        action_type,
        user,
        from_department=None,
        to_department=None,
        from_status="",
        to_status="",
        comment="",
    ):
        return WorkflowAction.objects.create(
            request=request,
            action_type=action_type,
            performed_by=user,
            from_department=from_department,
            to_department=to_department,
            from_status=from_status,
            to_status=to_status,
            comment=comment,
        )

    @staticmethod
    def _validate_user_department(user):
        if not user.department:
            raise PermissionDenied(
                "Your account is not assigned to a department."
            )

        if not user.is_active_employee:
            raise PermissionDenied(
                "Your employee account is inactive."
            )

    @staticmethod
    def _is_ed(user):
        return user.role == user.Role.EXECUTIVE_DIRECTOR

    @staticmethod
    def _is_ceo(user):
        return user.role == user.Role.CEO

    @staticmethod
    @transaction.atomic
    def submit(request, user):
        RequestWorkflowService._validate_user_department(user)

        if request.created_by_id != user.id:
            raise PermissionDenied(
                "Only the request creator can submit this request."
            )

        if not request.request_document:
            raise ValidationError(
                "A request document must be attached before submission."
            )

        if request.status != Request.Status.DRAFT:
            raise ValidationError(
                "Only draft requests can be submitted."
            )

        if request.destination_department.code == "CEO":
            raise PermissionDenied(
                "Departments cannot send requests directly to the CEO."
            )

        now = timezone.now()
        old_status = request.status

        request.status = Request.Status.SUBMITTED
        request.submitted_at = now

        request.save(
            update_fields=[
                "status",
                "submitted_at",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.SUBMITTED,
            user=user,
            from_department=request.originating_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
        )

        return request

    @staticmethod
    @transaction.atomic
    def receive(request, user):
        RequestWorkflowService._validate_user_department(user)

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You cannot receive a request assigned to another department."
            )

        if request.status not in [
            Request.Status.SUBMITTED,
            Request.Status.FORWARDED_TO_ED,
        ]:
            raise ValidationError(
                "This request cannot be received in its current state."
            )

        now = timezone.now()
        old_status = request.status

        request.status = Request.Status.RECEIVED
        request.received_at = now

        if RequestWorkflowService._is_ed(user):
            request.ed_received_at = now

        request.save(
            update_fields=[
                "status",
                "received_at",
                "ed_received_at",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.RECEIVED,
            user=user,
            from_department=request.originating_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
        )

        return request

    @staticmethod
    @transaction.atomic
    def approve(request, user, comment=""):
        RequestWorkflowService._validate_user_department(user)

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You cannot approve a request assigned to another department."
            )

        if request.status not in [
            Request.Status.RECEIVED,
            Request.Status.UNDER_REVIEW,
            Request.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This request cannot be approved in its current state."
            )

        old_status = request.status

        request.status = Request.Status.APPROVED

        request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.APPROVED,
            user=user,
            from_department=request.destination_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def reject(request, user, comment=""):
        RequestWorkflowService._validate_user_department(user)

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You cannot reject a request assigned to another department."
            )

        if request.status not in [
            Request.Status.RECEIVED,
            Request.Status.UNDER_REVIEW,
            Request.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This request cannot be rejected in its current state."
            )

        old_status = request.status

        request.status = Request.Status.REJECTED

        request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.REJECTED,
            user=user,
            from_department=request.destination_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def return_request(request, user, comment=""):
        RequestWorkflowService._validate_user_department(user)

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You cannot return a request assigned to another department."
            )

        if request.status not in [
            Request.Status.RECEIVED,
            Request.Status.UNDER_REVIEW,
            Request.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This request cannot be returned in its current state."
            )

        old_status = request.status

        request.status = Request.Status.RETURNED

        request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.RETURNED,
            user=user,
            from_department=request.destination_department,
            to_department=request.originating_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def forward_to_ed(request, user, comment=""):
        """
        A receiving department forwards a request to the ED.

        This is NOT an ED-only action.
        Any authorized receiving department can perform it.
        """

        RequestWorkflowService._validate_user_department(user)

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You can only forward requests assigned to your department."
            )

        if RequestWorkflowService._is_ed(user):
            raise PermissionDenied(
                "The Executive Director does not need to forward "
                "a request to ED."
            )

        if request.status not in [
            Request.Status.RECEIVED,
            Request.Status.APPROVED,
            Request.Status.UNDER_REVIEW,
            Request.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This request cannot be forwarded to the "
                "Executive Director in its current state."
            )

        ed_department = Department.objects.filter(
            code="ED",
            is_active=True,
        ).first()

        if not ed_department:
            raise ValidationError(
                "The Executive Director department has not been configured."
            )

        old_department = request.destination_department
        old_status = request.status

        request.destination_department = ed_department
        request.status = Request.Status.FORWARDED_TO_ED
        request.ed_received_at = timezone.now()

        request.save(
            update_fields=[
                "destination_department",
                "status",
                "ed_received_at",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.FORWARDED_TO_ED,
            user=user,
            from_department=old_department,
            to_department=ed_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def forward_to_ceo(request, user, comment=""):
        """
        Only the Executive Director can forward a request to CEO.
        """

        RequestWorkflowService._validate_user_department(user)

        if not RequestWorkflowService._is_ed(user):
            raise PermissionDenied(
                "Only the Executive Director can forward requests to the CEO."
            )

        if request.destination_department_id != user.department_id:
            raise PermissionDenied(
                "You can only forward requests currently assigned to "
                "the Executive Director."
            )

        if request.status not in [
            Request.Status.RECEIVED,
            Request.Status.APPROVED,
            Request.Status.UNDER_REVIEW,
            Request.Status.IN_PROGRESS,
        ]:
            raise ValidationError(
                "This request cannot be forwarded to the CEO "
                "in its current state."
            )

        ceo = Department.objects.filter(
            code="CEO",
            is_active=True,
        ).first()

        if not ceo:
            raise ValidationError(
                "The CEO department has not been configured."
            )

        ed_department = user.department
        old_status = request.status
        now = timezone.now()

        request.destination_department = ceo
        request.status = Request.Status.FORWARDED_TO_CEO
        request.ed_forwarded_at = now
        request.ceo_received_at = now

        request.save(
            update_fields=[
                "destination_department",
                "status",
                "ed_forwarded_at",
                "ceo_received_at",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.FORWARDED_TO_CEO,
            user=user,
            from_department=ed_department,
            to_department=ceo,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def ceo_approve(request, user, comment=""):
        RequestWorkflowService._validate_user_department(user)

        if not RequestWorkflowService._is_ceo(user):
            raise PermissionDenied(
                "Only the CEO can approve CEO-level requests."
            )

        if request.destination_department.code != "CEO":
            raise PermissionDenied(
                "This request has not been routed to the CEO."
            )

        if request.status != Request.Status.FORWARDED_TO_CEO:
            raise ValidationError(
                "This request is not awaiting a CEO decision."
            )

        old_status = request.status

        request.status = Request.Status.CEO_APPROVED

        request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.CEO_APPROVED,
            user=user,
            from_department=request.destination_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request

    @staticmethod
    @transaction.atomic
    def ceo_reject(request, user, comment=""):
        RequestWorkflowService._validate_user_department(user)

        if not RequestWorkflowService._is_ceo(user):
            raise PermissionDenied(
                "Only the CEO can reject CEO-level requests."
            )

        if request.destination_department.code != "CEO":
            raise PermissionDenied(
                "This request has not been routed to the CEO."
            )

        if request.status != Request.Status.FORWARDED_TO_CEO:
            raise ValidationError(
                "This request is not awaiting a CEO decision."
            )

        old_status = request.status

        request.status = Request.Status.CEO_REJECTED

        request.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        RequestWorkflowService._record_action(
            request=request,
            action_type=WorkflowAction.ActionType.CEO_REJECTED,
            user=user,
            from_department=request.destination_department,
            to_department=request.destination_department,
            from_status=old_status,
            to_status=request.status,
            comment=comment,
        )

        return request