import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from vectordb.models import Vector 
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query: return render(request, 'knowledge/search.html')

    # 1. Search the Cache first (Case-insensitive)
    cache = SearchHistory.objects.filter(
        query__iexact=query, 
        is_queued=False
    ).exclude(ai_response__icontains="Generating").first()

    if cache:
        return render(request, 'knowledge/search_results.html', {
            'query': query, 
            'answer': cache.ai_response, 
            'confidence': cache.confidence_score,
            'status': cache.rag_status(), 
            'history_id': cache.id, 
            'is_queued': False,
            'articles': [a.__dict__ for a in cache.source_articles.all()] 
        })

    # 2. PIGGYBACK LOGIC (CURRENTLY QUEUED)
    # If a user refreshes the page, piggyback on the active ticket instead of duplicating
    queued_history = SearchHistory.objects.filter(
        query__iexact=query,
        is_queued=True
    ).first()

    if queued_history:
        return render(request, 'knowledge/search_results.html', {
            'query': query,
            'answer': "",
            'confidence': queued_history.confidence_score,
            'status': queued_history.rag_status(),
            'history_id': queued_history.id,
            'articles': [a.__dict__ for a in queued_history.source_articles.all()],
            'is_queued': True 
        })

    # 3. No cache? Perform Vector Search and Queue it
    results = Vector.objects.search(query, k=3)
    found_articles = [res.metadata for res in results]
    
    total_score = sum(getattr(r, 'score', 0) for r in results) if results else 0
    confidence = min(100, int((total_score / 3) * 100))

    # Create the record for the worker
    history = SearchHistory.objects.create(
        query=query, 
        is_queued=True,
        ai_response="",
        confidence_score=confidence,
        needs_documentation=True if confidence < 50 else False
    )
    
    # Link documents so the worker knows what to read
    for res in results:
        art = Article.objects.filter(slug=res.metadata.get('slug')).first()
        if art: history.source_articles.add(art)

    return render(request, 'knowledge/search_results.html', {
        'query': query, 
        'answer': "", 
        'confidence': history.confidence_score,
        'status': history.rag_status(), 
        'history_id': history.id, 
        'is_queued': True, 
        'articles': found_articles
    })

def check_ai_status(request, history_id):
    """ Allows the frontend to check if the background worker is done """
    h = get_object_or_404(SearchHistory, id=history_id)
    return JsonResponse({
        'is_queued': h.is_queued, 
        'answer': h.ai_response if not h.is_queued else ""
    })

def article_detail(request, slug):
    """ View for individual article pages """
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'knowledge/article_detail.html', {'article': article})

def submit_feedback(request, history_id):
    """ Handles user feedback (Great/Meh/Nope) via AJAX """
    h = get_object_or_404(SearchHistory, id=history_id)
    if request.method == 'POST':
        h.user_feedback = int(request.POST.get('feedback'))
        if h.user_feedback == 3: # 'Nope'
            h.needs_documentation = True
        h.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def ollama_status_view(request):
    """ Lightweight ping to check if the local AI is awake """
    try:
        # A quick 2-second timeout check to see if Ollama is listening
        res = requests.get('http://localhost:11434/', timeout=2)
        if res.status_code == 200:
            return JsonResponse({'online': True})
    except Exception:
        pass
    
    return JsonResponse({'online': False})
