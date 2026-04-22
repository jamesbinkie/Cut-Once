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
    search_results = Vector.objects.search(query, k=3)
    
    context_list = []
    total_score = 0
    found_articles = []
    
    if search_results:
        for res in search_results:
            # FIX: The vector DB stores our model data inside a 'metadata' dictionary, not 'object'
            title = res.metadata.get('title', 'Unknown Title')
            content = res.metadata.get('content', '')
            
            context_list.append(f"Title: {title}\nContent: {content}")
            
            # Safely add the score (defaulting to 0 if missing)
            total_score += getattr(res, 'score', 0)
            
            # Add the metadata dictionary to our list so the HTML template can read the slug and title
            found_articles.append(res.metadata)

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
        }, timeout=120)
        
        # NEW: Force it to trigger the 'except' block if Ollama returns a 500 or 404 error
        response.raise_for_status() 
        
        # Extract the response safely
        ai_answer = response.json().get('response')
        
        # NEW: Catch if Ollama returned a 200 OK but the answer was completely blank
        if not ai_answer:
            ai_answer = "The AI returned an empty response. It might be struggling to process this request."

    except Exception as e:
        print(f"Ollama Error: {e}") # This will print the actual error to your terminal for debugging
        ai_answer = "Internal AI is currently offline or encountered an error. Please ensure Ollama is running properly."

    # 4. LOGGING: Track search history and knowledge gaps
    # Because we ensured ai_answer is ALWAYS a string now, the database won't crash!
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
        'history_id': history.id,
        'articles': found_articles  # <-- Now passing the valid metadata dictionaries
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
