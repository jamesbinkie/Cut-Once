import requests
import vectordb
from django.shortcuts import render
from .models import Article, SearchHistory

def ai_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'knowledge/search.html')

    # 1. RETRIEVAL: Find the most relevant internal documents
    # vectordb returns a similarity score we use for confidence
    search_results = vectordb.search(query, k=3)
    context_list = []
    total_similarity = 0
    
    for res in search_results:
        context_list.append(res.text)
        total_similarity += res.score # res.score is typically 0 to 1

    context_text = "\n---\n".join(context_list)
    
    # 2. CONFIDENCE CALCULATION
    # We normalize the vector similarity into a 0-100 percentage
    base_confidence = min(100, int((total_similarity / 3) * 100)) if context_list else 0

    # 3. GENERATION: Ask Local Ollama for a summary
    # We explicitly tell it NOT to use external knowledge
    prompt = f"""
    You are an internal assistant. Use ONLY the following internal documentation to answer.
    If the answer is not in the documentation, say "I do not have enough information."
    
    DOCUMENTS:
    {context_text}
    
    USER QUESTION: {query}
    """
    
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }, timeout=10)
        ai_answer = response.json().get('response', 'AI failed to respond.')
    except:
        ai_answer = "Local AI is currently offline."

    # 4. SAVE TO HISTORY (Knowledge Gap Detection)
    history = SearchHistory.objects.create(
        query=query,
        ai_response=ai_answer,
        confidence_score=base_confidence,
        needs_documentation=True if base_confidence < 50 else False
    )

    return render(request, 'knowledge/search_results.html', {
        'query': query,
        'answer': ai_answer,
        'confidence': base_confidence,
        'status': history.rag_status(),
        'history_id': history.id
    })
