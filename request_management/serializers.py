from rest_framework import serializers

from departments.models import Department

from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    request_document_url = serializers.SerializerMethodField()

    originating_department_name = serializers.CharField(
        source="originating_department.name",
        read_only=True,
    )

    destination_department_name = serializers.CharField(
        source="destination_department.name",
        read_only=True,
    )

    destination_department_code = serializers.CharField(
        source="destination_department.code",
        read_only=True,
    )

    class Meta:
        model = Request

        fields = (
            "id",
            "request_number",
            "subject",
            "description",
            "request_document",
            "request_document_url",
            "priority",
            "status",
            "created_by",
            "created_by_name",
            "originating_department",
            "originating_department_name",
            "destination_department",
            "destination_department_name",
            "destination_department_code",
            "required_by",
            "created_at",
            "submitted_at",
            "received_at",
            "ed_received_at",
            "ed_forwarded_at",
            "ceo_received_at",
            "completed_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "request_number",
            "status",
            "created_by",
            "created_at",
            "submitted_at",
            "received_at",
            "ed_received_at",
            "ed_forwarded_at",
            "ceo_received_at",
            "completed_at",
            "updated_at",
            "originating_department",
            "request_document_url",
        )

    def get_created_by_name(self, obj):
        return (
            obj.created_by.get_full_name()
            or obj.created_by.username
        )

    def get_request_document_url(self, obj):
        if not obj.request_document:
            return None

        request = self.context.get("request")

        url = obj.request_document.url

        if request:
            return request.build_absolute_uri(url)

        return url

    def validate_destination_department(self, value):
        if value.code == "CEO":
            raise serializers.ValidationError(
                "Requests cannot be sent directly to the CEO. "
                "Only the Executive Director can forward a "
                "request to the CEO."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user

        if not user.department:
            raise serializers.ValidationError(
                "Your account is not assigned to a department."
            )

        validated_data["created_by"] = user
        validated_data["originating_department"] = user.department

        return Request.objects.create(
            **validated_data
        )


class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request

        fields = (
            "subject",
            "description",
            "request_document",
            "priority",
            "destination_department",
            "required_by",
        )

    def validate_destination_department(self, value):
        if value.code == "CEO":
            raise serializers.ValidationError(
                "Requests cannot be sent directly to the CEO. "
                "Only the Executive Director can forward a "
                "request to the CEO."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user

        if not user.department:
            raise serializers.ValidationError(
                "Your account is not assigned to a department."
            )

        return Request.objects.create(
            created_by=user,
            originating_department=user.department,
            **validated_data,
        )