from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from vectordb.models import Vector 
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'knowledge/search.html')

    # --- 1. CACHE-FIRST LOGIC ---
    # Check if we already answered this exact question and it is finished generating
    cached_history = SearchHistory.objects.filter(
        query__iexact=query, 
        is_queued=False
    ).exclude(ai_response="").first()

    if cached_history:
        # Instant load! Return the cached answer
        return render(request, 'knowledge/search_results.html', {
            'query': query,
            'answer': cached_history.ai_response,
            'confidence': cached_history.confidence_score,
            'status': cached_history.rag_status(),
            'history_id': cached_history.id,
            'articles': cached_history.source_articles.all(),
            'is_queued': False
        })

    # --- 2. RETRIEVAL (Vector Database Search) ---
    search_results = Vector.objects.search(query, k=3)
    
    total_score = 0
    found_articles = []
    
    if search_results:
        for res in search_results:
            total_score += getattr(res, 'score', 0)
            # Retrieve the actual Article object using the primary key from metadata
            pk = res.metadata.get('pk')
            if pk:
                try:
                    article_obj = Article.objects.get(pk=pk)
                    found_articles.append(article_obj)
                except Article.DoesNotExist:
                    pass
    
    # --- 3. CONFIDENCE CALCULATION ---
    avg_score = (total_score / 3) if search_results else 0
    confidence = min(100, int(avg_score * 100))

    # --- 4. BACKGROUND QUEUEING ---
    # Create the search ticket so the worker script can pick it up
    history = SearchHistory.objects.create(
        query=query,
        ai_response="",  # Empty because the worker will generate it
        confidence_score=confidence,
        needs_documentation=True if confidence < 50 else False,
        is_queued=True   # ⏳ Flags it for the background worker!
    )
    
    # Attach the found articles to the ticket so the worker can read them
    if found_articles:
        history.source_articles.set(found_articles)

    return render(request, 'knowledge/search_results.html', {
        'query': query,
        'answer': "", # Template will show the loading spinner/typewriter
        'confidence': confidence,
        'status': history.rag_status(),
        'history_id': history.id,
        'articles': found_articles,
        'is_queued': True # Tells the Javascript to start polling
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'knowledge/article_detail.html', {'article': article})

def submit_feedback(request, history_id):
    history = get_object_or_404(SearchHistory, id=history_id)
    if request.method == 'POST':
        feedback_value = request.POST.get('feedback')
        history.user_feedback = int(feedback_value)
        if history.user_feedback == 3: # 'Nope'
            history.needs_documentation = True
        history.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# --- NEW: Polling Endpoint for Javascript ---
def check_status(request, history_id):
    """ Allows the frontend to check if the worker is finished """
    history = get_object_or_404(SearchHistory, id=history_id)
    return JsonResponse({
        'is_queued': history.is_queued,
        'ai_response': history.ai_response
    })
