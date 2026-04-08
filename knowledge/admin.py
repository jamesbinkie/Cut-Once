from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    list_filter = ('owner', 'last_reviewed')
    search_fields = ('title', 'content')

    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<b style="color: red;">⚠️ NEEDS REVIEW</b>')
        return format_html('<b style="color: green;">✅ CURRENT</b>')
    
    review_status.short_description = "Status"
