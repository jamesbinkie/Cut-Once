from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ('knowledge/js/page_builder.js',)
        css = {
            'all': ('knowledge/css/admin_builder.css',)
        }
    
    # Make sure this is indented to be EXACTLY in line with 'class Media:' above it!
    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"
