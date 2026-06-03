from django.db import models


class Task(models.Model):
	PRIORITY_CHOICES = [
		(1, "Low"),
		(2, "Medium"),
		(3, "High"),
	]
	STATUS_CHOICES = [
		("pending", "Pending"),
		("in_progress", "In Progress"),
		("completed", "Completed")
	]

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=2)
	status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="todo")
	deadline = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.title
