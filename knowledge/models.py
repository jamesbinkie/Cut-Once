from django.db import models
from django.utils import timezone
from datetime import timedelta

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="The URL name (e.g., 'office-security')")
    content = models.TextField(blank=True, help_text="Use the editor below to format your document.")
    owner = models.CharField(max_length=100)
    last_reviewed = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.title

    @property
    def needs_review(self):
        return timezone.now().date() > self.last_reviewed + timedelta(days=180)
