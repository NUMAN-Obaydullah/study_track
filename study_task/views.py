from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from .forms import TaskForm
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")
    context = {
        "username": "Numan",
        "tasks": tasks,
        "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],
    }
    return render(request, "task_list.html", context)


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
    return render(request, "home.html", context)

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
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_form.html", {"form": form, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],})
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
    return redirect("task_list")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form, "menu_items": [
            {"label": "Home", "url": "/"},
            {"label": "About", "url": "/about/"},
            {"label": "Tasks", "url": "/tasks/"},
        ],})