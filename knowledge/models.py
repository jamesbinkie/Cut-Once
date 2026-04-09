from django.db import models
from django.utils import timezone
from datetime import timedelta

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # This stores our list of widgets: [{'type': 'text', 'value': '...'}, {'type': 'html', 'value': '...'}]
    content_blocks = models.JSONField(default=list, blank=True) 
    
    owner = models.CharField(max_length=100)
    last_reviewed = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.title

    @property
    def needs_review(self):
        # Returns True if the article hasn't been reviewed in 180 days
        return timezone.now().date() > self.last_reviewed + timedelta(days=180)
