from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.utils.html import format_html
from .models import Article

# --- 1. HIERARCHY & UI CLEANUP ---
class CustomUserAdmin(UserAdmin):
    # This removes the "User Permissions" box so you only see "Groups"
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups", # We keep Groups but hide individual perms
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Tier 1 Protection: Hide Super-Admins from everyone except other Super-Admins
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

    def has_change_permission(self, request, obj=None):
        # Tier 1 Protection: Admins cannot edit Super-Admins
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Tier 1 Protection: Admins cannot delete Super-Admins
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

# Re-register the User model with our clean UI and protection logic
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
