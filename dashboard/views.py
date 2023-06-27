from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from dashboard.forms import (
    TaskForm,
    TaskSearchForm,
    TaskFilterForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    WorkerSearchForm,
    WorkerFilterForm,
)

from dashboard.models import Task, TaskType, Position, Worker


@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_position = Position.objects.count()
    num_workers = get_user_model().objects.count()

    context = {
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_position": num_position,
        "num_workers": num_workers,
    }

    return render(request, "dashboard/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "dashboard/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("dashboard:task-type-list")
    template_name = "dashboard/task_type_confirm_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("dashboard:position-list")
    template_name = "dashboard/position_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})
        context["filter_form"] = TaskFilterForm(initial=self.request.GET)

        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        filter_ = TaskFilterForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        if filter_.is_valid() and filter_.cleaned_data["priority"]:
            queryset = queryset.filter(
                priority=filter_.cleaned_data["priority"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("assignees__position")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("dashboard:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
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


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks__task_type")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("dashboard:worker-list")
