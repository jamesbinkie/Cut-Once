import requests
from vectordb import search  # Updated import logic
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'knowledge/search.html')

    # 1. RETRIEVAL: Using the corrected search function
    # search() returns a list of results with .text and .score
    search_results = search(query, k=3)
    context_list = [res.text for res in search_results]
    context_text = "\n---\n".join(context_list)
    
    # 2. CONFIDENCE CALCULATION
    avg_score = sum([res.score for res in search_results]) / 3 if search_results else 0
    confidence = min(100, int(avg_score * 100))

    # 3. GENERATION: Ask Ollama (llama3.2:1b)
    prompt = f"Use ONLY this info: {context_text}\n\nQuestion: {query}"
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }, timeout=15)
        ai_answer = response.json().get('response')
    except:
        ai_answer = "Internal AI is currently offline. Please ensure Ollama is running."

    # 4. LOGGING: Create the history record
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
