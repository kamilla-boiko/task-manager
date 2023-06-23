from django.contrib.auth import get_user_model
from django.test import TestCase

from dashboard.models import Task, TaskType, Position


class TaskTypeModelTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")

        self.assertEqual(str(task_type), task_type.name)


class PositionModelTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="test")

        self.assertEqual(str(position), position.name)


class WorkerModelTests(TestCase):
    def test_worker_str(self):
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            position=position
        )

        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position.name})"
        )

    def test_get_absolute_url(self):
        worker = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )

        self.assertEqual(
            worker.get_absolute_url(),
            f"/dashboard/workers/{worker.id}/"
        )


class TaskModelTests(TestCase):
    def test_task_str(self):
        task_type = TaskType.objects.create(name="test")
        task = Task.objects.create(
            name="Test",
            description="test test test",
            deadline="2023-07-07",
            is_completed=True,
            priority="Urgent",
            task_type=task_type
        )

        self.assertEqual(
            str(task),
            f"{task.name} ({task.priority}, deadline {task.deadline})"
        )

    def test_get_absolute_url(self):
        task_type = TaskType.objects.create(name="test")
        task = Task.objects.create(
            name="Test",
            description="test test test",
            deadline="2023-07-07",
            is_completed=True,
            priority="Urgent",
            task_type=task_type
        )

        self.assertEqual(
            task.get_absolute_url(),
            f"/dashboard/tasks/{task.id}/"
        )
