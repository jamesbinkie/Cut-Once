from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # Paths are relative to the static folder. 
        # v=3000 ensures a hard refresh of the browser cache.
        js = ('knowledge/js/page_builder.js?v=3000',)
        css = {
            'all': ('knowledge/css/admin_builder.css?v=3000',)
        }
    
    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"
