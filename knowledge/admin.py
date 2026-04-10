from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ('knowledge/js/Page_Builder_Final.js',)  # <-- MUST BE EXACTLY THIS
        css = {
            'all': ('knowledge/css/admin_builder.css',)
        }
    
    def review_status(self, obj):
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"

    # --- ADDED THIS TO SET DEFAULT USER ---
    def get_changeform_initial_data(self, request):
        # Grabs standard defaults, then overrides 'owner' with the logged-in user
        initial = super().get_changeform_initial_data(request)
        initial['owner'] = request.user
        return initial
