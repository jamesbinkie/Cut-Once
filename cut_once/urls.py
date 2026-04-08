from django.contrib import admin
from django.urls import path, include # Add 'include' here
from knowledge import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_search, name='home'),
    
    # This line adds login, logout, password resets, etc.
    path('accounts/', include('django.contrib.auth.urls')), 
]
