from django.shortcuts import render

from dashboard.models import Task, Worker


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
