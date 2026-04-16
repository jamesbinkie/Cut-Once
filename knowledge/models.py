from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Content', config_name='default', blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_reviewed = models.DateField(default=timezone.now)

    # Added: This tells the AI what to index for search
    def get_vectordb_text(self):
        return f"Title: {self.title}\nContent: {self.content}"

    def __str__(self):
        return self.title

class SearchHistory(models.Model):
    query = models.CharField(max_length=500)
    ai_response = models.TextField()
    
    # Certainty Metrics
    confidence_score = models.IntegerField(default=0) # 0-100%
    
    # Feedback Loop: 1=Great, 2=Meh, 3=Nope
    FEEDBACK_CHOICES = [(1, 'Great'), (2, 'Meh'), (3, 'Nope')]
    user_feedback = models.IntegerField(choices=FEEDBACK_CHOICES, null=True, blank=True)
    
    # Knowledge Gap Flag
    needs_documentation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def rag_status(self):
        """Returns the RAG color based on confidence."""
        if self.confidence_score >= 80: return 'green'
        if self.confidence_score >= 50: return 'amber'
        return 'red'
