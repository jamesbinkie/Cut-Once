from django.contrib import admin
from django.urls import path
from knowledge import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Fixed the '手' typo here
    path('', views.home_search, name='home'),
]
