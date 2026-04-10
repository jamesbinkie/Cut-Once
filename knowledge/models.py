from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth.models import User # <-- Added User import

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True) 
    
    # --- UPDATED FIELD ---
    # Links to Django's User table. Limits the dropdown to users who can access the admin panel.
    owner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'is_staff': True},
        verbose_name="Person to Review"
    )
    
    last_reviewed = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def needs_review(self):
        return timezone.now().date() > self.last_reviewed + timedelta(days=180)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
