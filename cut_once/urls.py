from django.contrib import admin
from django.urls import path, include 
from knowledge import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Updated to use the new AI search view
    path('', views.ai_search_view, name='home'),
    
    path('article/<slug:slug>/', views.article_detail, name='article_detail'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
    # New endpoint for the feedback buttons
    path('feedback/<int:history_id>/', views.submit_feedback, name='submit_feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
