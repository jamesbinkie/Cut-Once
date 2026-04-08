from django.contrib import admin
from django.urls import path
from knowledge import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.手admin.site.urls),
    path('', views.home_search, name='home'), # This sets the landing page
]
