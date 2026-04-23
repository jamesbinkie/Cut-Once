from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from vectordb.models import Vector 
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'knowledge/search.html')

    # 1. RETRIEVAL: Instant Vector Search
    search_results = Vector.objects.search(query, k=3)
    
    total_score = 0
    found_articles = []
    article_objects = [] # We need the actual database objects for the queue
    
    if search_results:
        for res in search_results:
            title = res.metadata.get('title', 'Unknown Title')
            
            # Save score and metadata for the frontend template
            total_score += getattr(res, 'score', 0)
            found_articles.append(res.metadata)
            
            # Grab the actual Article objects from the database to link to our Cache
            slug = res.metadata.get('slug')
            if slug:
                try:
                    article_objects.append(Article.objects.get(slug=slug))
                except Article.DoesNotExist:
                    pass

    avg_score = (total_score / 3) if search_results else 0
    confidence = min(100, int(avg_score * 100))

    # 2. CHECK THE CACHE (Has this been asked and rated 'Great'?)
    # We do a loose case-insensitive search for the exact query
    cached_history = SearchHistory.objects.filter(
        query__iexact=query,
        user_feedback=1, # 1 = Great!
        is_queued=False
    ).first()

    if cached_history:
        # CACHE HIT! Serve the saved answer instantly.
        ai_answer = cached_history.ai_response
        status = cached_history.rag_status()
        history_id = cached_history.id
        
    else:
        # 3. NO CACHE / NEW QUESTION: Send it to the background queue!
        ai_answer = "⏳ This is a new question! Our AI is currently reading the documents and generating a summary in the background. The answer will be cached for future searches shortly."

        history = SearchHistory.objects.create(
            query=query,
            ai_response=ai_answer,
            confidence_score=confidence,
            is_queued=True,  # <-- This tells your worker script to wake up!
            needs_documentation=True if confidence < 50 else False
        )
        
        # Link the source articles so the worker knows what to read
        for article in article_objects:
            history.source_articles.add(article)

        status = history.rag_status()
        history_id = history.id

    # 4. INSTANT PAGE LOAD
    # Cloudflare will never time out because this takes milliseconds!
    return render(request, 'knowledge/search_results.html', {
        'query': query,
        'answer': ai_answer,
        'confidence': confidence,
        'status': status,
        'history_id': history_id,
        'articles': found_articles 
    })

# ... keep your existing article_detail and submit_feedback views below ...
