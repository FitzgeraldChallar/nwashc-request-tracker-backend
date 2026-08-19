from django.urls import path

from .views import (
    CEOApproveView,
    CEORejectView,
    RequestApproveView,
    RequestDetailView,
    RequestForwardToCEOView,
    RequestForwardToEDView,
    RequestHistoryView,
    RequestListCreateView,
    RequestReceiveView,
    RequestRejectView,
    RequestReturnView,
    RequestSubmitView,
)


urlpatterns = [
    path(
        "",
        RequestListCreateView.as_view(),
        name="request-list-create",
    ),

    path(
        "<int:pk>/",
        RequestDetailView.as_view(),
        name="request-detail",
    ),

    path(
        "<int:pk>/submit/",
        RequestSubmitView.as_view(),
        name="request-submit",
    ),

    path(
        "<int:pk>/receive/",
        RequestReceiveView.as_view(),
        name="request-receive",
    ),

    path(
        "<int:pk>/approve/",
        RequestApproveView.as_view(),
        name="request-approve",
    ),

    path(
        "<int:pk>/reject/",
        RequestRejectView.as_view(),
        name="request-reject",
    ),

    path(
        "<int:pk>/return/",
        RequestReturnView.as_view(),
        name="request-return",
    ),

    path(
        "<int:pk>/forward-to-ed/",
        RequestForwardToEDView.as_view(),
        name="request-forward-to-ed",
    ),

    path(
        "<int:pk>/forward-to-ceo/",
        RequestForwardToCEOView.as_view(),
        name="request-forward-to-ceo",
    ),

    path(
        "<int:pk>/ceo-approve/",
        CEOApproveView.as_view(),
        name="ceo-approve",
    ),

    path(
        "<int:pk>/ceo-reject/",
        CEORejectView.as_view(),
        name="ceo-reject",
    ),

    path(
        "<int:pk>/history/",
        RequestHistoryView.as_view(),
        name="request-history",
    ),
]