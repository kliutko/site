from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

class Article(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    description = models.TextField()
    structure = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'