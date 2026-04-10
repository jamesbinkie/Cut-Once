from django.shortcuts import render, get_object_or_404 # <-- Added get_object_or_404
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

# --- ADD THIS NEW VIEW ---
@login_required
def article_detail(request, slug):
    # This finds the exact article or returns a 404 Not Found if it doesn't exist
    article = get_object_or_404(Article, slug=slug) 
    return render(request, 'knowledge/article_detail.html', {'article': article})
