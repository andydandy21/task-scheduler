from django.db import models
from django.urls import reverse

class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=1000)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('month-view')