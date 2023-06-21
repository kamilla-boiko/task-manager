from django.urls import path

from dashboard.views import index, TaskTypeListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    )
]

app_name = "dashboard"
