from django.db import models

# Create your models here.

class TodoModel(models.Model):
    task     = models.CharField(max_length=300)
    isActive = models.BooleanField(default=True)
    time     = models.DateTimeField()