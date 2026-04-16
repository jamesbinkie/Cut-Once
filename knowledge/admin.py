from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Article

# --- 1. HIERARCHY & AUTOMATION ---
class CustomUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        """ Dynamically hide fields based on who is logged in. """
        fieldsets = list(super().get_fieldsets(request, obj))
        
        # Find the 'Permissions' section in the admin form
        for name, field_options in fieldsets:
            if name == 'Permissions':
                fields = list(field_options.get('fields', []))
                
                # 1. Remove 'user_permissions' (the huge messy list) for everyone
                if 'user_permissions' in fields:
                    fields.remove('user_permissions')
                
                # 2. Remove 'is_staff' - we will automate this instead
                if 'is_staff' in fields:
                    fields.remove('is_staff')
                
                # 3. Remove 'is_superuser' if the logged-in user isn't a Super-Admin
                if not request.user.is_superuser and 'is_superuser' in fields:
                    fields.remove('is_superuser')
                
                field_options['fields'] = tuple(fields)
        return tuple(fieldsets)

    def save_model(self, request, obj, form, change):
        """ 
        Automatically set 'is_staff' to True if the user is placed 
        in a group (like your Admin group).
        """
        # If they are in any group, they are likely an Admin and need backend access
        if obj.groups.exists():
            obj.is_staff = True
        else:
            # If they have no groups, they are a General user (no backend access)
            obj.is_staff = False
            
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """ Hide Super-Admins from the user list for standard Admins. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

# Re-register User with these refined rules
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
        if obj.needs_review:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠️ NEEDS REVIEW')
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', '✅ CURRENT')

    review_status.short_description = "Status"

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['owner'] = request.user
        return initial
