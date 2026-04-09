from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # Storing everything as a single HTML string for the Google Docs feel
    content = models.TextField(blank=True) 
    
    owner = models.CharField(max_length=100)
    last_reviewed = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
