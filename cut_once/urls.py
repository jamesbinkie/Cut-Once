from django.contrib import admin
from django.urls import path, include 
from knowledge import views
from django.conf import settings # Added
from django.conf.urls.static import static # Added

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_search, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # CKEditor 5 URL
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
