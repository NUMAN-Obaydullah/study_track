from . models import Task
from django import forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "deadline"]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            'priority': forms.Select(attrs={"class": "form-control"}),          
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "created_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }