from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Added 'review_status' here so it actually appears in the list view
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # Added ?v=1 to force the browser to update the script and CSS
        js = ('knowledge/js/page_builder.js?v=1',)
        css = {
            'all': ('knowledge/css/admin_builder.css?v=1',)
        }
    
    def review_status(self, obj):
        # Displays the status based on the 180-day review logic in models.py
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ NEEDS REVIEW</span>')
        return format_html('<span style="color: green; font-weight: bold;">✅ CURRENT</span>')

    review_status.short_description = "Status"
