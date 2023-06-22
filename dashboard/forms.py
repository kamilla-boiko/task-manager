from django import forms
from django.contrib.auth import get_user_model

from dashboard.models import Task


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
