from django.urls import path

from dashboard.views import (
    index,
    TaskTypeListView,
    PositionListView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    )
]

app_name = "dashboard"
