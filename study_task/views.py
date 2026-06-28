from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from django import forms
from django.core.exceptions import PermissionDenied
from users_app.models import CustomUser
from .forms import TaskForm
from .models import Task
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")
    context = {
        "username": request.user.username,
        "tasks": tasks,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    }
    return render(request, "task_list.html", context)


def _add_bootstrap_classes(form):
    for name, field in form.fields.items():
        classes = field.widget.attrs.get("class", "")
        if "form-control" not in classes:
            field.widget.attrs["class"] = (classes + " form-control").strip()


def dashboard(request):
    tasks = Task.objects.all().order_by("-created_at")
    context = {
        "tasks": tasks,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    }
    return render(request, "dashboard.html", context)





def about(request):
    context = {"menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],}
    return render(request, "about.html", context)


def home(request):
    # Landing page - pass features to be rendered by base.html loop
    features = [
        {"title": "Organize", "text": "Group and prioritize your study tasks."},
        {"title": "Track", "text": "Keep track of deadlines and progress."},
        {"title": "Focus", "text": "Boost productivity with clear priorities."},
    ]
    context = {
        "username": "Numan",
        "appname": "Study Track",
        "features": features,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    }
    return render(request, "home.html", {"user": request.user, "menu_items": context["menu_items"], "features": context["features"]})
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {"task": task, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],}
    return render(request, "task_detail.html", context)
#task_create, task_edit, and task_delete views V1 - using request.POST directly without forms. This is less secure and more error-prone, but shown here for completeness.
# def task_create(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         priority = request.POST.get("priority", 2)
#         status = request.POST.get("status", "Pending")
#         deadline = request.POST.get("deadline")
#         task = Task.objects.create(
#             title=title,
#             description=description,
#             priority=priority,
#             status=status,
#             deadline=deadline if deadline else None,
#         )
#         return redirect("task_list")
#     return render(request, "task_form.html", {"menu_items": [
#             {"label": "Home", "url": "/"},
#             {"label": "About", "url": "/about/"},
#             {"label": "Tasks", "url": "/tasks/"},
#         ],})




# def task_edit(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == "POST":
#         task.title = request.POST.get("title")
#         task.description = request.POST.get("description")
#         task.priority = request.POST.get("priority", 2)
#         task.status = request.POST.get("status", "Pending")
#         deadline = request.POST.get("deadline")
#         task.deadline = deadline if deadline else None
#         task.save()
#         return redirect("task_list")
#     return render(request, "task_form.html", {"task": task, "menu_items": [
#             {"label": "Home", "url": "/"},
#             {"label": "About", "url": "/about/"},
#             {"label": "Tasks", "url": "/tasks/"},
#         ],})

# def task_delete(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == "POST":
#         task.delete()
#     return redirect("task_list")
# USING FORMS - more secure and robust way to handle create/edit operations, with built-in validation and error handling.
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],})
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        original_title = task.title
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if request.user.role != "MANAGER" and not request.user.is_superuser:
                form.instance.title = original_title
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_form.html", {
        "form": form,
        "task": task,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    })
@login_required
def task_delete(request, pk):
    if request.user.role != "MANAGER" and not request.user.is_superuser:
        # messages.error(request, "You do not have permission to delete tasks.")
        # return redirect("task_list")
        raise PermissionDenied("You do not have permission to delete tasks.")
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
    return redirect("task_list")
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        
        fields = ("username", "password1", "password2", "email", "phone_number")
        # fields = UserCreationForm.Meta.fields + ("email", "phone_number",)
class CustomUserCreationWithRoleForm(UserCreationForm):
    # 1. Field definitions go outside of the Meta class
    role = forms.ChoiceField(choices=[], required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # UserCreationForm inherently includes the password fields, 
        # so we just add the standard fields plus your custom ones.
        fields = ("username", "email", "phone_number", "role")

    def __init__(self, *args, **kwargs):
        # 2. Extract creator_role from kwargs before calling super()
        # Default to None if not provided
        creator_role = kwargs.pop('creator_role', None) 
        
        super().__init__(*args, **kwargs)
        
        # 3. Dynamically set the choices based on the creator's role
        if creator_role == 'ADMIN':
            self.fields['role'].choices = [
                ('ADMIN', 'Admin'),
                ('MANAGER', 'Manager'),
                ('EMPLOYEE', 'Employee'),
            ]
        elif creator_role == 'MANAGER':
            self.fields['role'].choices = [
                ('MANAGER', 'Manager'),
                ('EMPLOYEE', 'Employee'),
            ]
        else:
            # Fallback for safety (e.g., if somehow a regular employee reaches this form)
            self.fields['role'].choices = [
                ('EMPLOYEE', 'Employee'),
            ]
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        _add_bootstrap_classes(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()
        _add_bootstrap_classes(form)
    return render(request, "register.html", {"form": form, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],})
@login_required
def register_with_role(request):
    if request.user.role not in ["ADMIN", "MANAGER"] and not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to register a user.")
        
    creator_role = 'ADMIN' if request.user.is_superuser else request.user.role
    if request.method == 'POST':
        form = CustomUserCreationWithRoleForm(
            request.POST, 
            creator_role=creator_role
        )
        _add_bootstrap_classes(form)
        if form.is_valid():
            form.save()
            messages.success(request, "New user created successfully.")
            return redirect("dashboard")
    else:
        form = CustomUserCreationWithRoleForm(
            creator_role=creator_role
        )
        _add_bootstrap_classes(form)
    
    context = {
        "form": form,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    }
    return render(request, 'create_user.html', context)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        _add_bootstrap_classes(form)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm(request)
        _add_bootstrap_classes(form)
    return render(request, "login.html", {"form": form, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],})


def logout_view(request):
    logout(request)
    return redirect("home")
