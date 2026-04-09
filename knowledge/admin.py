from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # We use the full path relative to the STATIC_URL
        js = ('knowledge/js/page_builder.js?v=99',)
        css = {
            'all': ('knowledge/css/admin_builder.css?v=99',)
        }
    
    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ NEEDS REVIEW</span>')
        return format_html('<span style="color: green; font-weight: bold;">✅ CURRENT</span>')

    review_status.short_description = "Status"
