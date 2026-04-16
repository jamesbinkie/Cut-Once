from django.contrib import admin
from django.utils.html import format_html
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Display columns in the admin list view
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    # Automatically creates the slug based on the title
    prepopulated_fields = {"slug": ("title",)}

    # We removed the custom Page_Builder_Final.js because CKEditor 5 
    # handles the saving logic automatically.
    class Media:
        css = {
            'all': ('django_ckeditor_5/dist/styles.css',),
        }
        js = ('django_ckeditor_5/dist/bundle.js',)
    
    def review_status(self, obj):
        """Adds a visual badge to the list view for review status."""
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"

    def get_changeform_initial_data(self, request):
        """Automatically sets the 'Person to Review' to the current user."""
        initial = super().get_changeform_initial_data(request)
        initial['owner'] = request.user
        return initial
