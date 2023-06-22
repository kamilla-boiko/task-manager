from django.urls import path

from dashboard.views import (
    index,
    TaskTypeListView,
    PositionListView,
    TaskListView,
    WorkerListView,
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
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
]

app_name = "dashboard"
