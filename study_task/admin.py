from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("title", "created_at", "priority", "status", "deadline","description")
	list_filter = ("priority", "status")
	search_fields = ("title", "description")
	list_editable = ("priority", "status", "description") # can not be link and should be in list_display
	

	fieldsets = (
		("Basic Information", {"fields": ("title", "description")}),
		("Task Details", {"fields": ("priority", "status", "deadline")}),
	)