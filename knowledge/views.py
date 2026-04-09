def home_search(request):
    query = request.GET.get('q')
    articles = []
    if query:
        articles = Article.objects.filter(content__icontains=query)
    
    return render(request, 'knowledge/search.html', {
        'query': query,
        'articles': articles
    })
