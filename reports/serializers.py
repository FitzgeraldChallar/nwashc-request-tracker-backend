from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    draft = serializers.IntegerField()
    submitted = serializers.IntegerField()
    received = serializers.IntegerField()
    under_review = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    pending_information = serializers.IntegerField()
    returned = serializers.IntegerField()
    approved = serializers.IntegerField()
    rejected = serializers.IntegerField()
    completed = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    forwarded_to_ceo = serializers.IntegerField()


class DashboardRecentRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    request_number = serializers.CharField()
    subject = serializers.CharField()
    status = serializers.CharField()
    status_label = serializers.CharField()
    priority = serializers.CharField()
    priority_label = serializers.CharField()
    originating_department = serializers.CharField()
    destination_department = serializers.CharField()
    created_by = serializers.CharField()
    created_at = serializers.DateTimeField()
    submitted_at = serializers.DateTimeField(allow_null=True)


class EDDashboardSerializer(serializers.Serializer):
    summary = DashboardSummarySerializer()
    awaiting_ed_action = serializers.IntegerField()
    eligible_for_ceo_forwarding = serializers.IntegerField()
    forwarded_to_ceo = serializers.IntegerField()
    recent_requests = DashboardRecentRequestSerializer(many=True)


class DepartmentDashboardSerializer(serializers.Serializer):
    department = serializers.DictField()
    summary = DashboardSummarySerializer()
    sent = serializers.IntegerField()
    received = serializers.IntegerField()
    pending = serializers.IntegerField()
    approved = serializers.IntegerField()
    denied = serializers.IntegerField()
    recent_requests = DashboardRecentRequestSerializer(many=True)


class CEODashboardSerializer(serializers.Serializer):
    summary = DashboardSummarySerializer()
    awaiting_ceo_action = serializers.IntegerField()
    approved_by_ceo = serializers.IntegerField()
    rejected_by_ceo = serializers.IntegerField()
    recent_requests = DashboardRecentRequestSerializer(many=True)
    