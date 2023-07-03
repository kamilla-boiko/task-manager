from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from dashboard.forms import (
    validate_deadline,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    WorkerSearchForm,
    WorkerFilterForm,
    TaskSearchForm,
    TaskFilterForm,
)
from dashboard.models import Position


class WorkerFormsTests(TestCase):
    def test_worker_creation_form_with_first_last_name_email_position(self):
        position = Position.objects.create(name="position")
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "email": "user@user.com",
            "position": position,
        }
        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update_form_only_position(self):
        position = Position.objects.create(name="position")
        worker = get_user_model().objects.create(
            username="existing_user",
            password="password",
            first_name="Existing first",
            last_name="Existing last",
            email="existing@user.com",
            position=position,
        )

        form_data = {
            "position": Position.objects.create(name="updated_position")
        }
        form = WorkerPositionUpdateForm(data=form_data, instance=worker)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["position"], form_data["position"])

    def test_worker_search_form(self):
        form_data_valid = {"username": "searched_user"}
        form = WorkerSearchForm(data=form_data_valid)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"], form_data_valid["username"]
        )

        form_data_invalid = {"username": ""}
        form_invalid = WorkerSearchForm(data=form_data_invalid)

        self.assertTrue(form_invalid.is_valid())
        self.assertEqual(form_invalid.cleaned_data["username"], "")

    def test_worker_filter_form(self):
        position = Position.objects.create(name="position1")
        form_data_valid = {"position": position.id}
        form_valid = WorkerFilterForm(data=form_data_valid)

        self.assertTrue(form_valid.is_valid())
        self.assertEqual(form_valid.cleaned_data["position"], position)

        form_data_invalid = {}
        form_invalid = WorkerFilterForm(data=form_data_invalid)

        self.assertTrue(form_invalid.is_valid())
        self.assertIsNone(form_invalid.cleaned_data["position"])


class TaskFormsTests(TestCase):
    def test_task_search_form(self):
        form_data_valid = {"name": "searched_name"}
        form = TaskSearchForm(data=form_data_valid)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data_valid["name"])

        form_data_invalid = {"name": ""}
        form_invalid = TaskSearchForm(data=form_data_invalid)

        self.assertTrue(form_invalid.is_valid())
        self.assertEqual(form_invalid.cleaned_data["name"], "")

    def test_task_filter_form(self):
        form_data_valid = {"priority": "Urgent"}
        form_valid = TaskFilterForm(data=form_data_valid)

        self.assertTrue(form_valid.is_valid())
        self.assertEqual(
            form_valid.cleaned_data["priority"], form_data_valid["priority"]
        )

        form_data_invalid = {}
        form_invalid = TaskFilterForm(data=form_data_invalid)

        self.assertTrue(form_invalid.is_valid())
        self.assertEqual(form_invalid.cleaned_data["priority"], "")


class ValidDeadlineTests(TestCase):
    def test_correct_deadline(self):
        deadline = date(2023, 7, 30)

        self.assertEqual(validate_deadline(deadline), deadline)

    def test_deadline_not_earlier_than_current_date(self):
        deadline = date(2023, 6, 22)
        message = "Deadline cannot be earlier than current date"

        with self.assertRaisesMessage(ValidationError, message):
            validate_deadline(deadline)
