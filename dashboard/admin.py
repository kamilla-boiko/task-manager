from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dashboard.models import Task, TaskType, Position, Worker


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "priority", "task_type")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "position")}),
    )


admin.site.register(TaskType)
admin.site.register(Position)
