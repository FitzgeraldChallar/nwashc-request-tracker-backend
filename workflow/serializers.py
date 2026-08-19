from rest_framework import serializers

from .models import WorkflowAction


class WorkflowActionSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.SerializerMethodField()

    from_department_name = serializers.CharField(
        source="from_department.name",
        read_only=True,
    )

    to_department_name = serializers.CharField(
        source="to_department.name",
        read_only=True,
    )

    action_label = serializers.CharField(
        source="get_action_type_display",
        read_only=True,
    )

    class Meta:
        model = WorkflowAction
        fields = (
            "id",
            "action_type",
            "action_label",
            "performed_by",
            "performed_by_name",
            "from_department",
            "from_department_name",
            "to_department",
            "to_department_name",
            "from_status",
            "to_status",
            "comment",
            "created_at",
        )

        read_only_fields = fields

    def get_performed_by_name(self, obj):
        return (
            obj.performed_by.get_full_name()
            or obj.performed_by.username
        )