from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dashboard.models import Task, TaskType, Position

TASK_URL = reverse("dashboard:task-list")
TASK_TYPE_URL = reverse("dashboard:task-type-list")
POSITION_URL = reverse("dashboard:position-list")
WORKER_URL = reverse("dashboard:worker-list")


class PublicTaskTypeViewTest(TestCase):
    def test_task_type_list_login_required(self):
        res = self.client.get(TASK_TYPE_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicPositionViewTest(TestCase):
    def test_position_list_login_required(self):
        res = self.client.get(POSITION_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicTaskViewTest(TestCase):
    def test_task_list_login_required(self):
        res = self.client.get(TASK_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicWorkerViewTest(TestCase):
    def test_worker_list_login_required(self):
        res = self.client.get(WORKER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="Test name 1")
        TaskType.objects.create(name="Test name 2")

        response = self.client.get(TASK_TYPE_URL)

        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types)
        )
        self.assertTemplateUsed(response, "dashboard/task_type_list.html")


class PrivatePositionViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        Position.objects.create(name="Test name 1")
        Position.objects.create(name="Test name 2")

        response = self.client.get(POSITION_URL)

        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertTemplateUsed(response, "dashboard/position_list.html")


class PrivateTaskViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_tasks(self):
        task_type = TaskType.objects.create(name="test")
        Task.objects.create(
            name="Test 1",
            description="test test test",
            deadline="2023-07-08",
            is_completed=True,
            priority="Urgent",
            task_type=task_type
        )
        Task.objects.create(
            name="Test 2",
            description="test test test",
            deadline="2023-07-07",
            is_completed=True,
            priority="Urgent",
            task_type=task_type
        )

        response = self.client.get(TASK_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertTemplateUsed(response, "dashboard/task_list.html")


class PrivateWorkerViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_workers(self):
        get_user_model().objects.create_user(
            username="test1",
            password="test12345",
        )
        get_user_model().objects.create_user(
            username="test2",
            password="test12345",
        )

        response = self.client.get(WORKER_URL)

        workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "dashboard/worker_list.html")

    def test_create_worker(self):
        position = Position.objects.create(name="position")
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position.id
        }
        self.client.post(reverse("dashboard:worker-create"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position, position)
