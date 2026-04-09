from django.contrib import admin
from django.utils.html import format_html
from .models import Article

from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        # We will create this JS file next to handle the "Add/Remove" buttons
        js = ('knowledge/js/page_builder.js',)
        css = {
            'all': ('knowledge/css/admin_builder.css',)
        }
    
    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ NEEDS REVIEW</span>')
        return format_html('<span style="color: green; font-weight: bold;">✅ CURRENT</span>')

    review_status.short_description = "Status"
