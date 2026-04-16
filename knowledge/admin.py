from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Article

# --- PROTECT SUPER ADMINS ---
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If the logged-in person is NOT a Super-Admin, hide all Super-Admins from the list
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

    def has_change_permission(self, request, obj=None):
        # Prevent non-superusers from editing superusers
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Only Super-Admins can delete other Super-Admins
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

# Re-register User with our new protected rules
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- ARTICLE ADMIN (Your existing code + CKEditor) ---
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
