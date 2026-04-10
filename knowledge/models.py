from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

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

    # Django Admin automatically looks for this exact function to add a "View on Site" button
    def get_absolute_url(self):
        # Assuming your url pattern is named 'article_detail' in knowledge/urls.py
        return reverse('article_detail', kwargs={'slug': self.slug})
