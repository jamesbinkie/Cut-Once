from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def health_check(request):
    return HttpResponse("Wooo Its working!")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", health_check, name="health_check"),
]
