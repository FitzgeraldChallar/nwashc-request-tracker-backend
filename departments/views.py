from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.filter(
            is_active=True
        ).order_by("name")

        serializer = DepartmentSerializer(
            departments,
            many=True,
        )

        return Response(serializer.data)