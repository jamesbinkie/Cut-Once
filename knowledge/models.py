from django.db import models
from django.utils import timezone
from datetime import timedelta

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True) # Must be 'content'
    owner = models.CharField(max_length=100)
    last_reviewed = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def needs_review(self):
        return timezone.now().date() > self.last_reviewed + timedelta(days=180)
