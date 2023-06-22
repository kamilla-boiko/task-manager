from django.urls import path

from dashboard.views import (
    index,
    TaskTypeListView,
    PositionListView,
    TaskListView
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
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    )
]

app_name = "dashboard"
