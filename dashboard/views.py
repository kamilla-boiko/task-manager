from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from dashboard.forms import TaskForm, WorkerCreationForm, WorkerPositionUpdateForm, WorkerSearchForm, WorkerFilterForm
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


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_form.html"


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_confirm_delete.html"


class PositionListView(generic.ListView):
    model = Position


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_form.html"


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_form.html"


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_confirm_delete.html"


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related("task_type")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees__position")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("dashboard:task-list")


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        context["filter_form"] = WorkerFilterForm(initial=self.request.GET)

        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        filter_ = WorkerFilterForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        if filter_.is_valid() and filter_.cleaned_data["position"]:
            queryset = queryset.filter(
                position=filter_.cleaned_data["position"]
            )

        return queryset


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks__task_type")


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerPositionUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("dashboard:worker-list")
