from django.shortcuts import render  # <--- This is the missing line
from django.contrib.auth.decorators import login_required
from .models import Article

@login_required
def home_search(request):
    query = request.GET.get('q')
    articles = []
    
    if query:
        # This searches for your query in the content of your articles
        articles = Article.objects.filter(content__icontains=query)
    
    return render(request, 'knowledge/search.html', {
        'query': query,
        'articles': articles
    })
