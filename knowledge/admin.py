from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # Paths relative to the static folder
        js = ('knowledge/js/page_builder.js?v=9999',)
        css = {
            'all': ('knowledge/css/admin_builder.css?v=9999',)
        }
    
    def review_status(self, obj):
        # Placeholder {} is required by format_html in modern Django
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"
