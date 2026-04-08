from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_search(request):
    return render(request, 'knowledge/search.html')
