from django.contrib import admin
from django.urls import path, include 
from knowledge import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Match the URL path '/search' that caused the 404
    path('search/', views.ai_search_view, name='home'),
    
    # Redirect empty root to search if desired, or keep search on home
    path('', views.ai_search_view, name='index'), 
    
    path('article/<slug:slug>/', views.article_detail, name='article_detail'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/check-status/<int:history_id>/', views.check_ai_status, name='check_ai_status'),
    
    # Feedback endpoint for the AI results
    path('feedback/<int:history_id>/', views.submit_feedback, name='submit_feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
