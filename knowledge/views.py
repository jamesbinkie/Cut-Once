import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# Import the Vector model directly for searching
from vectordb.models import Vector 
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'knowledge/search.html')

    # 1. RETRIEVAL: Use the Vector model manager to search
    # This matches the query against your mathematically indexed articles
    search_results = Vector.objects.search(query, k=3)
    
    context_list = []
    total_score = 0
    for res in search_results:
        # res.object is the original Article instance
        context_list.append(f"Title: {res.object.title}\nContent: {res.object.content}")
        total_score += res.score

    context_text = "\n---\n".join(context_list)
    
    # 2. CONFIDENCE CALCULATION
    avg_score = (total_score / 3) if search_results else 0
    confidence = min(100, int(avg_score * 100))

    # 3. GENERATION: Request a summary from Local Ollama
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama3.2:1b",
            "prompt": f"Use ONLY this info: {context_text}\n\nQuestion: {query}",
            "stream": False
        }, timeout=15)
        ai_answer = response.json().get('response')
    except Exception:
        ai_answer = "Internal AI is currently offline. Please ensure Ollama is running."

    # 4. LOGGING: Track search history and knowledge gaps
    history = SearchHistory.objects.create(
        query=query,
        ai_response=ai_answer,
        confidence_score=confidence,
        needs_documentation=True if confidence < 50 else False
    )

    return render(request, 'knowledge/search_results.html', {
        'query': query,
        'answer': ai_answer,
        'confidence': confidence,
        'status': history.rag_status(),
        'history_id': history.id
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
