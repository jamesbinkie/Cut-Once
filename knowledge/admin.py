from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Article, SearchHistory 

# --- 1. HIERARCHY & AUTOMATION ---
class CustomUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        """ Dynamically hide fields based on who is logged in. """
        fieldsets = list(super().get_fieldsets(request, obj))
        
        for name, field_options in fieldsets:
            if name == 'Permissions':
                fields = list(field_options.get('fields', []))
                
                # Remove messy individual permissions for everyone
                if 'user_permissions' in fields:
                    fields.remove('user_permissions')
                
                # Remove 'is_staff' - we automate this via Groups
                if 'is_staff' in fields:
                    fields.remove('is_staff')
                
                # Hide 'is_superuser' from everyone except existing Super-Admins
                if not request.user.is_superuser and 'is_superuser' in fields:
                    fields.remove('is_superuser')
                
                field_options['fields'] = tuple(fields)
        return tuple(fieldsets)

    def save_model(self, request, obj, form, change):
        """ 
        Fixes the ValueError: Checks form data to see if a Group was 
        selected, then sets Staff status automatically.
        """
        # Look at the selected groups in the form before the user is saved
        selected_groups = form.cleaned_data.get('groups')
        
        if selected_groups and selected_groups.exists():
            obj.is_staff = True
        else:
            # If no groups are selected, they are a General user (no backend)
            obj.is_staff = False
            
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """ Protects Super-Admins from being seen or edited by standard Admins. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

# Re-register User with the fixed automation
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# --- 2. ARTICLE ADMIN (CKEditor Enabled) ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'last_reviewed', 'review_status')
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        css = {'all': ('django_ckeditor_5/dist/styles.css',)}
        js = ('django_ckeditor_5/dist/bundle.js',)
    
    def review_status(self, obj):
        if hasattr(obj, 'needs_review') and obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['owner'] = request.user
        return initial


# --- 3. SEARCH HISTORY ADMIN (Improved Tracking) ---
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    # What you see in the main list
    list_display = ('query', 'status_tag', 'user_feedback', 'created_at')
    
    # Adds filters on the right side for easy tracking
    list_filter = ('is_queued', 'user_feedback', 'needs_documentation')
    
    search_fields = ('query', 'ai_response')
    
    # Organize the detailed view
    readonly_fields = ('created_at', 'confidence_score')
    
    fieldsets = (
        ('Search Request', {
            'fields': ('query', 'created_at')
        }),
        ('AI Progress', {
            'fields': ('is_queued', 'ai_response', 'confidence_score')
        }),
        ('Human Review', {
            'fields': ('user_feedback', 'needs_documentation', 'admin_review_notes')
        }),
    )

  def status_tag(self, obj):
        """ Visual indicator of AI progress in the dashboard list """
        if getattr(obj, 'is_queued', False):
            # FIX: We now use '{}' as a placeholder and pass the text as an argument
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', '⏳ Thinking...')
        
        if obj.ai_response and "Generating" not in obj.ai_response:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ Ready')
            
        return format_html('<span style="color: gray;">{}</span>', 'Unknown')

    status_tag.short_description = "Status"

    def get_queryset(self, request):
        """Highlight queries that need articles written."""
        return super().get_queryset(request).order_by('-needs_documentation', '-created_at')
