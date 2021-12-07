from enum import Enum
from django.db import models

# Create your models here.
class Question(models.Model):
    name = models.TextField()
    # answers_count = models.PositiveSmallIntegerField()