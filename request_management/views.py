from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflow.models import WorkflowAction
from workflow.serializers import WorkflowActionSerializer
from workflow.services import RequestWorkflowService

from .models import Request
from .serializers import (
    RequestCreateSerializer,
    RequestSerializer,
)


class RequestListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.department:
            return Response(
                {
                    "detail": (
                        "Your account is not assigned "
                        "to a department."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        requests = (
            Request.objects.filter(
                Q(created_by=user)
                | Q(destination_department=user.department)
                | Q(originating_department=user.department)
            )
            .select_related(
                "created_by",
                "originating_department",
                "destination_department",
            )
            .distinct()
        )

        serializer = RequestSerializer(
            requests,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = RequestCreateSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        request_object = serializer.save()

        return Response(
            RequestSerializer(request_object).data,
            status=status.HTTP_201_CREATED,
        )


class RequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Request.objects.select_related(
                "created_by",
                "originating_department",
                "destination_department",
            ).get(pk=pk)
        except Request.DoesNotExist:
            return None

    def has_access(self, request_object, user):
        return (
            request_object.created_by_id == user.id
            or request_object.originating_department_id
            == user.department_id
            or request_object.destination_department_id
            == user.department_id
        )

    def get(self, request, pk):
        request_object = self.get_object(pk)

        if not request_object:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self.has_access(
            request_object,
            request.user,
        ):
            return Response(
                {
                    "detail": (
                        "You do not have access "
                        "to this request."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = RequestSerializer(request_object)

        return Response(serializer.data)


class RequestSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.submit(
                request_object,
                request.user,
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestReceiveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.receive(
                request_object,
                request.user,
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.approve(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.reject(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.return_request(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestForwardToEDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.forward_to_ed(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestForwardToCEOView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.forward_to_ceo(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CEOApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.ceo_approve(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CEORejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)

            updated_request = RequestWorkflowService.ceo_reject(
                request_object,
                request.user,
                request.data.get("comment", ""),
            )

            return Response(
                RequestSerializer(updated_request).data
            )

        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except (PermissionDenied, ValidationError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            request_object = Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        has_access = (
            request_object.created_by_id == request.user.id
            or request_object.originating_department_id
            == request.user.department_id
            or request_object.destination_department_id
            == request.user.department_id
        )

        if not has_access:
            return Response(
                {
                    "detail": (
                        "You do not have access "
                        "to this request."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        actions = (
            WorkflowAction.objects.filter(
                request=request_object
            )
            .select_related(
                "performed_by",
                "from_department",
                "to_department",
            )
        )

        return Response(
            WorkflowActionSerializer(
                actions,
                many=True,
            ).data
        )