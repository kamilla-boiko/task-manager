from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from dashboard.models import Task, TaskType, Position, Worker


def index(request):
    num_tasks = Task.objects.count()
    tasks_completed = Task.objects.filter(is_completed=True).count()
    tasks_uncompleted = num_tasks - tasks_completed

    context = {
        "num_tasks": num_tasks,
        "tasks_completed": tasks_completed,
        "tasks_uncompleted": tasks_uncompleted
    }

    return render(request, "dashboard/index.html", context=context)


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "dashboard/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_form.html"


class PositionListView(generic.ListView):
    model = Position


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related("task_type")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees__position")


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks__task_type")
