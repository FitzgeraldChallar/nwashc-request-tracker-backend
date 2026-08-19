from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CEODashboardSerializer,
    DepartmentDashboardSerializer,
    EDDashboardSerializer,
)
from .services import DashboardService


class DashboardView(APIView):
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

        # CEO
        if user.role == user.Role.CEO:
            data = DashboardService.ceo_dashboard()

            serializer = CEODashboardSerializer(data)

            return Response(serializer.data)

        # Executive Director
        if user.role == user.Role.EXECUTIVE_DIRECTOR:
            data = DashboardService.ed_dashboard()

            serializer = EDDashboardSerializer(data)

            return Response(serializer.data)

        # All other departments
        data = DashboardService.department_dashboard(user)

        serializer = DepartmentDashboardSerializer(data)

        return Response(serializer.data)