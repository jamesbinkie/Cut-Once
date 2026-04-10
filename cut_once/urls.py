from django.contrib import admin
from django.urls import path, include 
from knowledge import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_search, name='home'),
    
    # --- ADD THIS NEW LINE ---
    # This matches the 'article_detail' name your models.py is looking for
    path('article/<slug:slug>/', views.article_detail, name='article_detail'), 
    
    # This line adds login, logout, password resets, etc.
    path('accounts/', include('django.contrib.auth.urls')), 
]
