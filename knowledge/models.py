from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models.signals import post_save
from django.dispatch import receiver

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Content', config_name='default', blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_reviewed = models.DateField(default=timezone.now)

    # Required for AI Search: Tells the indexer what to read
    def get_vectordb_text(self):
        return f"Title: {self.title}\nContent: {self.content}"

    def __str__(self):
        return self.title

class SearchHistory(models.Model):
    query = models.CharField(max_length=500)
    ai_response = models.TextField()
    
    # NEW: Link the answer to the exact documents it used
    source_articles = models.ManyToManyField(Article, blank=True)
    
    # NEW: The Background Queue Flag
    is_queued = models.BooleanField(default=False, help_text="True if waiting for background AI generation")
    
    # Certainty Metrics
    confidence_score = models.IntegerField(default=0) # 0-100%
    
    # Feedback Loop: 1=Great, 2=Meh, 3=Nope
    FEEDBACK_CHOICES = [(1, 'Great'), (2, 'Meh'), (3, 'Nope')]
    user_feedback = models.IntegerField(choices=FEEDBACK_CHOICES, null=True, blank=True)
    
    # Knowledge Gap Flag & Admin Review Notes
    needs_documentation = models.BooleanField(default=False)
    admin_review_notes = models.TextField(blank=True, help_text="Notes from staff reviewing bad AI answers")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def rag_status(self):
        """Returns the color code for the certainty box."""
        if self.confidence_score >= 80: return 'green'
        if self.confidence_score >= 50: return 'amber'
        return 'red'

# NEW: The "Auto-Queue" Trigger
@receiver(post_save, sender=Article)
def queue_related_searches(sender, instance, **kwargs):
    """
    Any time an Article is edited and saved, this automatically finds 
    ALL cached AI answers that used it, and drops them back into the queue 
    to be regenerated so they stay accurate.
    """
    related_searches = instance.searchhistory_set.all()
    related_searches.update(is_queued=True)
